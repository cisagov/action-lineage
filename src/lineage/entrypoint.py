#!/usr/bin/env python3
"""GitHub Action to create pull requests for upstream changes."""

# Standard Python Libraries
import logging
import os
from pathlib import Path
import subprocess  # nosec
import sys
from typing import Generator, List, Optional, Tuple
from urllib.parse import ParseResult, urlparse

# Third-Party Libraries
from github import Github, Repository
import pkg_resources
import pystache
import requests
import yaml

# Constants
ALREADY_UP_TO_DATE = "Already up to date."
CONFIG_FILENAME = ".github/lineage.yml"
GIT = "/usr/local/bin/git"


def run(
    cmd: List[str],
    cwd: Optional[str] = None,
    comment: Optional[str] = None,
    error_ok: bool = False,
) -> subprocess.CompletedProcess:
    """Run a command and display its output and return code."""
    if comment:
        logging.info(f"💬 {comment}")
    logging.debug(f"➤  {cmd}")
    proc = subprocess.run(
        cmd,
        shell=False,  # nosec
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if proc.returncode == 0:
        logging.debug(proc.stdout.decode())
        logging.info("✅ success")
    elif error_ok:
        logging.debug(proc.stdout.decode())
        logging.info(f"✅ (error ok) return code: {proc.returncode}")
    else:
        logging.warning(proc.stdout.decode())
        logging.warning(f"❌ ERROR! return code: {proc.returncode}")
    return proc


def load_template(github_workspace_dir, default_filename, custom_filename=None):
    """Load specified template file or local default."""
    template_data: str
    if custom_filename:
        template_path: Path = Path(github_workspace_dir) / Path(custom_filename)
        logging.info(f"Loading template file: {template_path}")
        with template_path.open() as f:
            template_data: str = f.read()
    else:
        logging.info(f"Loading default template: {default_filename}")
        template_data = (
            pkg_resources.resource_string("lineage", f"templates/{default_filename}")
            .decode("utf-8")
            .strip()
        )
    return template_data


def get_repo_list(
    g: Github, repo_query: str
) -> Generator[Repository.Repository, None, None]:
    """Generate a list of repositories based on the query."""
    logging.info(f"Querying for repositories: {repo_query}")
    matching_repos = g.search_repositories(query=repo_query)
    for repo in matching_repos:
        yield repo


def get_config(repo) -> Optional[dict]:
    """Read the lineage configuration for this repo."""
    config_path: Path = (Path(repo.full_name) / Path(".github/lineage.yml"))
    if config_path.exists():
        with config_path.open() as f:
            return yaml.safe_load(f)
    else:
        return None


def switch_branch(repo, lineage_id, local_branch) -> Tuple[str, bool]:
    """Switch to the PR branch, and possibly create it."""
    branch_name = f"lineage/{lineage_id}"
    logging.info(f"Attempting to switch to branch: {branch_name}")
    proc = run([GIT, "switch", branch_name], cwd=repo.full_name, error_ok=True)
    if proc.returncode:
        # branch does not exist, create it
        logging.info(
            f"Branch did not exist.  Creating: {branch_name} from local {local_branch}"
        )
        logging.info(f"Creating branch {branch_name} from {local_branch}")
        run([GIT, "branch", branch_name, local_branch], cwd=repo.full_name)
        logging.info(f"Switching to {branch_name}")
        run([GIT, "switch", branch_name], cwd=repo.full_name)
        return branch_name, True  # branch is new
    else:
        return branch_name, False  # branch existed


def fetch(repo, remote_url, remote_branch):
    """Fetch commits from remote branch."""
    logging.info(f"Fetching {remote_url} {remote_branch}")
    run([GIT, "fetch", remote_url, remote_branch], cwd=repo.full_name)


def merge(repo) -> Tuple[bool, Optional[str]]:
    """Merge previously fetched commits."""
    conflict_diff: Optional[str] = None
    logging.info(f"Attempting merge of fetched changes.")
    proc = run([GIT, "merge", "--no-commit", "FETCH_HEAD"], cwd=repo.full_name)
    if ALREADY_UP_TO_DATE in proc.stdout.decode():
        logging.info("Branch is already up to date.")
        return False, conflict_diff
    conflict: bool = proc.returncode != 0
    if conflict:
        logging.info("Conflict detected during merge.  Collecting conflicted files.")
        proc = run([GIT, "diff", "--name-only", "--diff-filter=U"], cwd=repo.full_name)
        conflict_diff = proc.stdout.decode()
        logging.info("Adding conflicts into branch for later resolution.")
        run([GIT, "add", "."], cwd=repo.full_name)
    logging.info("Committing merge.")
    run([GIT, "commit", "--file=.git/MERGE_MSG"], cwd=repo.full_name)
    return True, conflict_diff


def push(repo, branch_name, username, password):
    """Push changes to remote."""
    parts: ParseResult = urlparse(repo.clone_url)
    cred_url = parts._replace(netloc=f"{username}:{password}@{parts.netloc}").geturl()
    logging.info("Assigning credentials for push.")
    run([GIT, "remote", "set-url", "origin", cred_url], cwd=repo.full_name)
    logging.info(f"Pushing {branch_name} to remote.")
    run([GIT, "push", "--set-upstream", "origin", branch_name], cwd=repo.full_name)


def create_pull_request(repo, pr_branch_name, local_branch, title, body, draft):
    """Create a pull request."""
    logging.info(f"Creating a new pull request in {repo.full_name}")
    repo.create_pull(
        title=title, head=pr_branch_name, base=local_branch, body=body, draft=draft
    )


def main() -> int:
    """Parse evironment and perform requested actions."""
    # Set up logging
    logging.basicConfig(format="%(levelname)s %(message)s", level="INFO")

    # Get inputs from the environment
    access_token: Optional[str] = os.environ.get("INPUT_ACCESS_TOKEN")
    github_workspace_dir: Optional[str] = os.environ.get("GITHUB_WORKSPACE")
    repo_query: Optional[str] = os.environ.get("INPUT_REPO_QUERY")

    # sanity checks
    if access_token is None:
        logging.fatal(
            "Access token environment variable must be set. (INPUT_ACCESS_TOKEN)"
        )
        return -1

    if github_workspace_dir is None:
        logging.fatal(
            "GitHub workspace environment variable must be set. (GITHUB_WORKSPACE)"
        )
        return -1

    if repo_query is None:
        logging.fatal(
            "Reository query environment variable must be set. (INPUT_REPO_QUERY)"
        )
        return -1

    # Ensure we are working in our workspace
    os.chdir(github_workspace_dir)

    # Create a Github access object
    g = Github(access_token)

    # Set up a session to do things the Github library has not yet implemented.
    session: requests.Session = requests.Session()
    session.auth = ("", access_token)

    clean_template = load_template(github_workspace_dir, "clean_template.md", None)
    conflict_template = load_template(
        github_workspace_dir, "conflict_template.md", None
    )

    repos = get_repo_list(g, repo_query)
    for repo in repos:
        logging.info(f"Checking: {repo.full_name}")
        logging.info(f"Cloning repository: {repo.clone_url}")
        run([GIT, "clone", repo.clone_url, repo.full_name])
        config = get_config(repo)
        if not config:
            logging.info("Repository configuration not detected.")
            continue
        logging.info("Repository configuration detected.")
        lineage_id: str
        local_branch: str
        remote_branch: Optional[str]
        remote_url: str
        for lineage_id, v in config["lineage"].items():
            local_branch = v["local-branch"]
            remote_branch = v.get("remote-branch")
            remote_url = v["remote-url"]
            logging.info(f"Processing lineage: {lineage_id}")
            logging.info(f"Upstream: {remote_url} {remote_branch or ''}")
            # Check to see if a PR branch already exists
            branch_is_new: bool
            branch_name: str
            pr_branch_name, branch_is_new = switch_branch(
                repo, lineage_id, local_branch
            )
            logging.info(f"Pull request branch is new: {branch_is_new}")
            fetch(repo, remote_url, remote_branch)
            changed: bool
            conflict_diff: Optional[str]
            changed, conflict_diff = merge(repo)
            if not changed:
                logging.info(
                    f"Already up to date with: {remote_url} {remote_branch or ''} "
                )
                continue
            push(repo, pr_branch_name, "git", access_token)

            if branch_is_new:
                logging.info("Creating a new pull request since branch is new.")
                template_data = {
                    "conflict_diff": conflict_diff,
                    "pr_branch_name": pr_branch_name,
                    "remote_branch": remote_branch,
                    "remote_url": remote_url,
                }
                if conflict_diff:
                    title = f"⚠️ CONFLICT! Lineage pull request for: {lineage_id}"
                    body = pystache.render(conflict_template, template_data)
                    create_pull_request(
                        repo, pr_branch_name, local_branch, title, body, draft=True
                    )
                else:
                    title = f"Lineage pull request for: {lineage_id}"
                    body = pystache.render(clean_template, template_data)
                    create_pull_request(
                        repo, pr_branch_name, local_branch, title, body, draft=False
                    )
            else:
                logging.info(
                    "Not creating a new pull request since the branch already existed."
                )

    logging.info("Completed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
