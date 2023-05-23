# Lineage Pull Request #

[Lineage] has created this pull request to incorporate new changes found in an
upstream repository:

Upstream repository: [`{{ remote_url }}`]({{ remote_url }})
{{#remote_branch}}Remote branch: `{{ remote_branch }}`{{/remote_branch}}

Check the changes in this pull request to ensure they won't cause issues with
your project.

## ✅ Pre-approval checklist ##

Remove any of the following that do not apply. If you're unsure about
any of these, don't hesitate to ask. We're here to help!

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

> **Note**
> You are seeing this because one of this repository's maintainers has
> configured [Lineage] to open pull requests.

For more information:

🛠 [Lineage] configurations for this project are stored in `.github/lineage.yml`

📚 [Read more about Lineage][Lineage]

[//]: # ({{ metadata }})
[Lineage]: https://github.com/cisagov/action-lineage/ "Lineage GitHub Action"
