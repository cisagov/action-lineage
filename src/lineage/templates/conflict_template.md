# Lineage Pull Request: CONFLICT #

<img align="left" width="100" src="https://raw.githubusercontent.com/cisagov/action-lineage/develop/src/achtung.gif">

[Lineage] has created this pull request to incorporate new changes found in an
upstream repository:

Upstream repository: [`{{ remote_url }}`]({{ remote_url }})
{{#remote_branch}}Remote branch: `{{ remote_branch }}`{{/remote_branch}}

Check the changes in this pull request to ensure they won't cause issues with
your project.

The `{{ pr_branch_name }}` branch has **one or more unresolved merge conflicts**
that you must resolve before merging this pull request!

## How to resolve the conflicts ##

1. Take ownership of this pull request by removing any other assignees.

1. Clone the repository locally, and reapply the merge:

    ```console
    git clone {{ ssh_url }} {{ repo_name }}
    cd {{ repo_name }}
    git remote add {{ lineage_id }} {{ remote_url }}
    git remote set-url --push {{ lineage_id }} no_push
    git switch {{ local_branch }}
    git switch --create {{ pr_branch_name }} --track origin/{{ local_branch }}
    git pull {{ lineage_id }} {{ remote_branch }}
    git status
    ```

1. Review the changes displayed by the `status` command.  Fix any conflicts and
   possibly incorrect auto-merges.

1. After resolving each of the conflicts, `add` your changes to the
   branch, `commit`, and `push` your changes:

    ```console
    git add {{#conflict_file_list}}{{.}} {{/conflict_file_list}}
    git commit
    git push --force --set-upstream origin {{ pr_branch_name }}
    ```

    Note that you may *append* to the default merge commit message
    that git creates for you, but *please do not delete the existing
    content*.  It provides useful information about the merge that is
    being performed.

1. Wait for all the automated tests to pass.

1. Confirm each item in the "Pre-approval checklist" below.

1. Remove any of the checklist items that do not apply.

1. Ensure every remaining checkbox has been checked.

1. Mark this draft pull request "Ready for review".

## ✅ Pre-approval checklist ##

Remove any of the following that do not apply. If you're unsure about
any of these, don't hesitate to ask. We're here to help!

- [ ] ✌️ The conflicts in this pull request have been resolved.
- [ ] *All* future TODOs are captured in issues, which are referenced
      in code comments.
- [ ] All relevant type-of-change labels have been added.
- [ ] All relevant repo and/or project documentation has been updated
      to reflect the changes in this PR.
- [ ] Tests have been added and/or modified to cover the changes in this PR.
- [ ] All new and existing tests pass.

## ✅ Pre-merge checklist ##

Remove any of the following that do not apply. These boxes should
remain unchecked until the pull request has been approved.

- [ ] Bump major, minor, patch, or pre-release version [as
      appropriate](https://semver.org/#semantic-versioning-specification-semver)
      via the `bump_version.sh` script *if* this repository is
      versioned *and* the changes in this PR [warrant a version
      bump](https://semver.org/#what-should-i-do-if-i-update-my-own-dependencies-without-changing-the-public-api).
- [ ] Finalize version.

## ✅ Post-merge checklist ##

Remove any of the following that do not apply.

- [ ] Create a release.

---

> [!NOTE]
> You are seeing this because one of this repository's maintainers has
> configured [Lineage] to open pull requests.

For more information:

🛠 [Lineage] configurations for this project are stored in `.github/lineage.yml`

📚 [Read more about Lineage][Lineage]

[//]: # ({{ metadata }})
[Lineage]: https://github.com/cisagov/action-lineage/ "Lineage GitHub Action"
