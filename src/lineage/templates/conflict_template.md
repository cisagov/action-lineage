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
    git checkout -b {{ pr_branch_name }} --track origin/{{ local_branch }}
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

1. Check the "Everything is cool" checkbox below.

1. Mark this draft pull request "Ready for review".

## ✅ Pre-approval checklist ##

<!-- Remove any of the following that do not apply. -->
<!-- Draft PRs should have one or more unchecked boxes. -->
<!-- If you're unsure about any of these, don't hesitate to ask. -->
<!-- We're here to help! -->

- [ ] ✌️ The conflicts in this pull request have been resolved.
- [ ] Changes are limited to a single goal - *eschew scope creep!*
- [ ] *All* future TODOs are captured in issues, which are referenced
      in code comments.
- [ ] All relevant type-of-change labels have been added.
- [ ] I have read the [CONTRIBUTING](../blob/develop/CONTRIBUTING.md) document.
- [ ] These code changes follow [cisagov code standards](https://github.com/cisagov/development-guide).
- [ ] All relevant repo and/or project documentation has been updated
      to reflect the changes in this PR.
- [ ] Tests have been added and/or modified to cover the changes in this PR.
- [ ] All new and existing tests pass.

## ✅ Pre-merge checklist ##

<!-- Remove any of the following that do not apply. -->
<!-- These boxes should remain unchecked until the pull request has been -->
<!-- approved. -->

- [ ] Bump version via the `bump_version.sh` script, if this
      repository is versioned.

## ✅ Post-merge checklist ##

<!-- Remove any of the following that do not apply. -->

- [ ] Create a release.

---

**Note:** *You are seeing this because one of this repository's maintainers has
configured [Lineage] to open pull requests.*

For more information:

🛠 [Lineage] configurations for this project are stored in `.github/lineage.yml`

📚 [Read more about Lineage][Lineage]

[//]: # ({{ metadata }})
[Lineage]: https://github.com/cisagov/action-lineage/ "Lineage GitHub Action"
