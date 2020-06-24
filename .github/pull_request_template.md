# Hey, I just made a Pull Request!

## Description
<!--- Describe your changes -->

## Motivation and Context
<!--- Why is this change required? What problem does it solve? -->
<!--- If it fixes an open issue, please link to the issue here. -->

## Have you tested this? If so, how?
<!--- Valid responses are "I have included unit tests." and -->
<!--- "I ran `interrogate` with these changes over some code and it works for me." -->

## Checklist for PR author(s)
<!-- If an item doesn't apply to your pull request, **check it anyway** to make it apparent that there's nothing left to do. -->
- [ ] Changes are covered by unit tests (no major decrease in code coverage %).
- [ ] All tests pass.
- [ ] Docstring coverage is **100%** via `tox -e docs` or `interrogate -c pyproject.toml` (I mean, we _should_ set a good example :smile:).
- [ ] Updates to documentation:
    - [ ] Document any relevant additions/changes in `README.rst`.
    - [ ] Manually update **both** the `README.rst` _and_ `docs/index.rst` for any new/changed CLI flags.
    - [ ] Any changed/added classes/methods/functions have appropriate `versionadded`, `versionchanged`, or `deprecated` [directives](http://www.sphinx-doc.org/en/stable/markup/para.html#directive-versionadded).  Find the appropriate next version in the project's [``__init__.py``](https://github.com/econchick/interrogate/blob/master/src/interrogate/__init__.py) file.

## Release note
<!--  If your change is non-trivial (e.g. more than a fixed typo in docs, or updated tests), please write a suggested release note for us to include in `docs/changelog.rst` (we may edit it a bit).

1. Enter your release note in the below block. If the PR requires additional action from users switching to the new release, start the release note with the string "action required: ". Please write it in the imperative.
2. If no release note is required, just write "NONE".
-->
```release-note

```

<!---
for more information on how to submit valuable contributions,
see https://opensource.guide/how-to-contribute/#how-to-submit-a-contribution
-->
