# action-lineage #

[![GitHub Build Status](https://github.com/cisagov/action-lineage/workflows/build/badge.svg)](https://github.com/cisagov/action-lineage/actions)
[![Lineage Scan Status](https://github.com/cisagov/action-lineage/workflows/lineage_scan/badge.svg)](https://github.com/cisagov/action-lineage/actions?query=workflow%3Alineage_scan)
[![CodeQL](https://github.com/cisagov/action-lineage/workflows/CodeQL/badge.svg)](https://github.com/cisagov/action-lineage/actions/workflows/codeql-analysis.yml)
[![Coverage Status](https://coveralls.io/repos/github/cisagov/action-lineage/badge.svg?branch=develop)](https://coveralls.io/github/cisagov/action-lineage?branch=develop)
[![Known Vulnerabilities](https://snyk.io/test/github/cisagov/action-lineage/develop/badge.svg)](https://snyk.io/test/github/cisagov/action-lineage)

A GitHub Action to automatically generate PR requests from upstream repositories
regardless of the fork network.

## Repository Lineage configuration ##

Lineage is configured using `.github/lineage.yml` in a repository.  Each
upstream repository is listed in the `lineage` section.

| Key | Description | Required |
|-----|-------------|:--------:|
| local-branch | The branch that will receive new changes. | No |
| remote-url   | The `https` URL of the upstream repository. | Yes |
| remote-branch | The branch in the upstream repository. | No |

Below is an example configuration that defines two upstream repositories. The
`skeleton` repository specifies both the source and destination branches, while
the `extra-sauce` repository uses the default branches for both repositories.

```yml
---
version: "1"

lineage:
  skeleton:
    local-branch: develop
    remote-url: https://github.com/cisagov/skeleton-generic.git
    remote-branch: develop
  extra-sauce:
    remote-url: https://github.com/felddy/extra-skel-sauce.git
```

## Usage ##

### Inputs ###

| Name | Description | Interpreted Type | Default | Required |
|------|-------------|------------------|---------|:--------:|
| access_token | GitHub personal access token (see [GitHub's documentation](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)). | `string` | n/a | yes |
| mask_non_public_repos | Whether to mask the names of non-public (`private` and `internal`) repositories in the GitHub Actions logs. | [`boolean`](https://yaml.org/spec/1.2.2/#1032-tag-resolution) | `true` | no |
| include_non_public_repos | Whether to process non-public (`private` and `internal`) repositories. | [`boolean`](https://yaml.org/spec/1.2.2/#1032-tag-resolution) | `false` | no |
| repo_query | GitHub search query to use when finding repositories for which to create pull requests (e.g. \"org:cisagov archived:false\"). | `string` | n/a | yes |

### Outputs ###

None.
<!--
| Name | Description | Output Type |
|------|-------------|-------------|
| output_name | The output's description. | `output_type` |
-->

### Sample GitHub Actions workflow ###

The Lineage action requires a personal access token so that it may open pull
requests.  For public repositories this token must have the `public_repo`
permission enabled.  The token is provided using the repository secrets.

```yml
---
name: lineage_scan

on:
  schedule:
    - cron: "0 0 * * *"

env:
  ACCESS_TOKEN: ${{ secrets.ACCESS_TOKEN }}

jobs:
  cisagov:
    runs-on: ubuntu-latest
    steps:
      - name: Check all organization repositories
        uses: cisagov/action-lineage@develop
        with:
          access_token: ${{ env.ACCESS_TOKEN }}
          repo_query: "org:cisagov archived:false"
```

## Contributing ##

We welcome contributions!  Please see [`CONTRIBUTING.md`](CONTRIBUTING.md) for
details.

## License ##

This project is in the worldwide [public domain](LICENSE).

This project is in the public domain within the United States, and
copyright and related rights in the work worldwide are waived through
the [CC0 1.0 Universal public domain
dedication](https://creativecommons.org/publicdomain/zero/1.0/).

All contributions to this project will be released under the CC0
dedication. By submitting a pull request, you are agreeing to comply
with this waiver of copyright interest.
