# rtlpy Contributor's Guide

## Verifying the Project

A ```tox``` environment has been setup to check the [coding styles](#Coding-Style) and the ```pytest``` tests.

## PyTest Tests
Testing for this project is done with ```pytest```.
These test's live in the ./tests directory.

## Coding Style
Coding style guidelines can be found [here](./CodingStyle.md)

Coding style requirements can be checked by running ```flake8 rtlpy tests``` from
  the project top directory.

Additionally, the static-typing requirement of the CodingStyle can be checked
  by running ```mypy rtlpy```

## Releasing

Releases are published automatically when a tag is pushed to GitHub.

```bash

  # Set next version number
  export RELEASE=x.x.x
  export RELEASE=export RELEASE=$(python -c "import rtlpy._info as _info; print(_info.__version__)")

  # Ensure committing everything (optional)
  git add -A

  # Create tags
  git commit --allow-empty -m "Release $RELEASE"
  git tag -a $RELEASE -m "Version $RELEASE"

  # Push
  git push --follow-tags
```