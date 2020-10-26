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
    git pull {{ lineage_id }} {{ remote_branch }}{{#display_lineage_config_skip}}
    git checkout --ours -- {{lineage_config_filename}}
    git add {{lineage_config_filename}}{{/display_lineage_config_skip}}
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

    Note that you may _append_ to the default merge commit message
    that git creates for you, but *please do not delete the existing
    content*.  It provides useful information about the merge that is
    being performed.

1. Wait for all the automated tests to pass.

1. Check the "Everything is cool" checkbox below:

    - [ ] ✌️ The conflicts in this pull request have been resolved.

1. Mark this draft pull request "Ready for review".

------------

**Note:** *You are seeing this because one of this repository's maintainers has
configured [Lineage] to open pull requests.*

For more information:

🛠 [Lineage] configurations for this project are stored in `.github/lineage.yml`

📚 [Read more about Lineage][Lineage]

[//]: # ({{ metadata }})
[Lineage]: https://github.com/cisagov/action-lineage/ "Lineage GitHub Action"
