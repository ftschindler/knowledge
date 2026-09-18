---
type: Tool
title: linkspector
description: A Markdown and AsciiDoc link checker that resolves each link twice, with an HTTP request
  first and a headless Chrome behind it, configured by a strictly validated .linkspector.yml.
tags:
- tools
- linkspector
- links
- pre-commit
- documentation
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-09-18T00:00:00Z'
sources:
- id: linkspector-repo
  resource: https://github.com/UmbrellaDocs/linkspector
  title: 'UmbrellaDocs/linkspector: Uncover broken links in your content'
  last_modified: '2026-09-18'
---
linkspector[^linkspector-repo] extracts every link from a set of Markdown or AsciiDoc files and
reports the ones that do not resolve. It is the link checker this bundle runs as a pre-commit
hook, and the tool the snippet in
[Pin transitive runtime dependencies, not just the tool](../principles/pin_transitive_runtime_dependencies_not_just_the_tool.md)
is drawn from.

| | |
| --- | --- |
| Author | Gaurav Nelson, under the `UmbrellaDocs` organisation |
| Licence | Apache-2.0 |
| Language | JavaScript |
| Distribution | npm, as `@umbrelladocs/linkspector`, and a GitHub Action, `UmbrellaDocs/action-linkspector` |
| Source | [github.com/UmbrellaDocs/linkspector](https://github.com/UmbrellaDocs/linkspector) |
| Version read | 0.5.3, with 0.5.6 the latest release |

## What it is

Each link is resolved twice, and knowing which pass answered is most of what makes its
behaviour legible. The **first pass** is an HTTP `HEAD` request, which settles anything that
returns a status. The **second pass** is a real page load in headless Chrome, driven by
Puppeteer, for the links the first pass could not settle. That second pass is why a link
checker needs a browser at all, and why the version of Chrome it drives is a dependency worth
pinning alongside the tool.

The two passes do not share code, so a configuration option is only in force for the pass that
reads it. That is not visible from the configuration file, and it is the shape of
[the httpHeaders finding](../findings/20260918_linkspector_ignores_the_httpheaders_in_its_config.md).

## How it is configured

`.linkspector.yml` names the files to scan and then modifies the link set before checking it.
`ignorePatterns` drops links matching a regular expression, `replacementPatterns` rewrites them
by regular expression with capture groups, and `aliveStatusCodes` widens what counts as
success. `httpHeaders` attaches headers to matching URLs, subject to the finding above.
Any `${VAR}` in the file is substituted from the environment before validation.

The configuration is validated against a strict schema, which rejects any key it does not
define, at the top level and inside a list entry alike:

```text
Validation Error: "privateOrgs" is not allowed
Validation Error: "ignorePatterns[0].reason" is not allowed
```

The practical consequence is that the file cannot be annotated in its own syntax. A pattern
cannot carry a `reason`, and a list the rest of a repository wants to share cannot be kept
here, so anything of that kind lives in another file with something to hold the two in
agreement.
