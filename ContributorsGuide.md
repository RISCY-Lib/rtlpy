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
