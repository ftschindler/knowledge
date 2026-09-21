# Guides

A procedure I have carried out and would carry out again, written so it can be followed
without rediscovering why each step is there.

A guide is not a [blueprint](../blueprints/index.md) and the split is worth holding onto: a
blueprint is the artefact a decision produced, a thing to copy, whilst a guide is a sequence of
acts to perform in the world. Most of what makes a guide worth keeping is not the steps, which
any vendor's documentation also has, but the two or three of them that are easy to skip and
silent when skipped. Those are the reason the page exists, so they are marked rather than left
to be inferred.

Here that means three conventions. **Say what happens when a step is missed**, beside the step
itself, because a procedure that only describes success teaches nothing about the failure it is
written to prevent. **Separate what is done once by hand from what lives in a repository**: the
two are maintained by different people at different times, and a page that interleaves them
leaves a reader unable to tell what they are supposed to have already. And **name the version or
date of the interface being driven**, since a guide is a claim about somebody else's console
and those get redesigned; the reasoning is
[Date a page whose claim is about a version](../knowledge_management/date_a_page_whose_claim_is_about_a_version.md).

- [Let CI push to a protected branch with a GitHub App](let_ci_push_to_a_protected_branch_with_a_github_app.md) - an App installed on one repository, minting an hour-long token, instead of a maintainer's personal token in a secret
