#!/usr/bin/env python3
"""GitHub Action to rebuild respositories that haven't be built in a while."""

# Standard Python Libraries
from datetime import datetime
import logging
import os
import sys
from typing import Generator, Optional

# Third-Party Libraries
from dateutil.parser import isoparse
from dateutil.relativedelta import relativedelta
from github import Github, Repository
import pytimeparse
import requests


def get_repo_list(
    g: Github, repo_query: str
) -> Generator[Repository.Repository, None, None]:
    """Generate a list of repositories based on the query."""
    print(f"Querying for repositories: {repo_query}")
    matching_repos = g.search_repositories(query=repo_query)
    for repo in matching_repos:
        yield repo


def get_last_run(
    session: requests.Session, repo: Repository.Repository, workflow_id: str
) -> Optional[datetime]:
    """Get the last run time for a workflow in a respository."""
    logging.debug(f"Requesting workflow runs for repository {repo.name}")
    response = session.get(
        f"https://api.github.com/repos/{repo.full_name}/actions/workflows/{workflow_id}/runs"
    )
    if response.status_code != 200:
        logging.debug(
            f"No previous runs for {workflow_id} in {repo.full_name}, {response.status_code}"
        )
        return None
    workflow_runs = response.json()["workflow_runs"]
    if len(workflow_runs) == 0:
        return None
    else:
        last_run_date = workflow_runs[0]["created_at"]
        return isoparse(last_run_date).replace(tzinfo=None)


def main() -> int:
    """Parse evironment and perform requested actions."""
    # Set up logging
    logging.basicConfig(format="%(asctime)-15s %(levelname)s %(message)s", level="INFO")

    # Get inputs from the environment
    access_token: Optional[str] = os.environ.get("INPUT_ACCESS_TOKEN")
    build_age: Optional[str] = os.environ.get("INPUT_BUILD_AGE")
    event_type: Optional[str] = os.environ.get("INPUT_EVENT_TYPE")
    repo_query: Optional[str] = os.environ.get("INPUT_REPO_QUERY")
    workflow_id: Optional[str] = os.environ.get("INPUT_WORKFLOW_ID")
    max_rebuilds: int = int(os.environ.get("INPUT_MAX_REBUILDS", 10))

    # sanity checks
    if access_token is None:
        logging.fatal(
            "Access token environment variable must be set. (INPUT_ACCESS_TOKEN)"
        )
        return -1

    if build_age is None:
        logging.fatal("Build age environment variable must be set. (INPUT_BUILD_AGE)")
        return -1

    if event_type is None:
        logging.fatal("Event type environment variable must be set. (INPUT_EVENT_TYPE)")
        return -1

    if repo_query is None:
        logging.fatal(
            "Reository query environment variable must be set. (INPUT_REPO_QUERY)"
        )
        return -1

    if workflow_id is None:
        logging.fatal(
            "Workflow ID environment variable must be set. (INPUT_WORKFLOW_ID)"
        )
        return -1

    # setup time calculations
    now: datetime = datetime.utcnow()
    build_age_seconds: int = pytimeparse.parse(build_age)
    time_delta: relativedelta = relativedelta(seconds=build_age_seconds)
    past_date: datetime = now - time_delta

    logging.info(f"Rebuilding repositories that haven't run since {past_date}")

    # Create a Github access object
    g = Github(access_token)

    # Set up a session to do things the Github library has not yet implemented.
    session: requests.Session = requests.Session()
    session.auth = ("", access_token)

    repos = get_repo_list(g, repo_query)

    rebuilds_triggered = 0
    for repo in repos:
        last_run = get_last_run(session, repo, workflow_id)
        if last_run is None:
            continue
        if last_run < past_date:
            logging.info(f"{repo.full_name} needs a rebuild: {now - last_run}")
            if max_rebuilds == 0 or rebuilds_triggered < max_rebuilds:
                rebuilds_triggered += 1
                repo.create_repository_dispatch(event_type)
                logging.info(
                    f"Sent {event_type} event #{rebuilds_triggered} to {repo.full_name}."
                )
                if rebuilds_triggered == max_rebuilds:
                    logging.warning("Max rebuild events sent.")
        else:
            logging.info(f"{repo.full_name} is OK: {now - last_run}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
