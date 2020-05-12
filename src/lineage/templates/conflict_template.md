# Lineage Pull Request: CONFLICT #

![DANGER](https://raw.githubusercontent.com/cisagov/action-lineage/develop/src/achtung.gif)

[Lineage] has created this pull request to incorporate new changes found in an
upstream repository:

Upstream repository: [`{{ remote_url }}`]({{ remote_url }})
{{#remote_branch}}Remote branch: `{{ remote_branch }}`{{/remote_branch}}

Check the changes in this pull request to ensure they won't cause issues with
your project.

The `{{ pr_branch_name }}` branch has **one or more unresolved merge conflicts**
that you must resolve before merging this pull request!

## How to resolve the conflicts ##

1. Clone the `{{ pr_branch_name }}` branch locally:

    ```console
    git clone --single-branch --branch {{ pr_branch_name }} {{ ssh_url }}
    ```

1. Review each of the following files looking for [conflict-resolution markers](https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging#_basic_merge_conflicts):

    ```console
    {{#conflict_file_list}}
    {{.}}
    {{/conflict_file_list}}
    ```

1. Resolve each of the conflicts and `add` your changes to the branch:

    ```console
    git add {{#conflict_file_list}}{{.}} {{/conflict_file_list}}
    ```

1. Once all the changes have been added, `commit` and `push` the changes back to
GitHub:

    ```console
    git commit --message="Resolved Lineage conflicts."
    git push
    ```

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
