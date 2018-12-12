# pytest-patterns

[![Build Status](https://travis-ci.org/smarie/pytest-patterns.svg?branch=master)](https://travis-ci.org/smarie/pytest-patterns) [![Documentation](https://img.shields.io/badge/docs-latest-blue.svg)](https://smarie.github.io/pytest-patterns/)

A couple of examples showing how to use core `pytest` mechanisms and existing plugins (no additional hooks or hacks) to solve real-world problems. In other words:
 
    "pytest for humans ;)"

**This is the readme for developers.** The documentation for users is available here: [https://smarie.github.io/pytest-patterns/](https://smarie.github.io/pytest-patterns/)


## Want to contribute ?

Contributions are welcome ! Simply fork this project on github, commit your contributions, and create pull requests.

Here is a non-exhaustive list of interesting open topics: [https://github.com/smarie/pytest-patterns/issues](https://github.com/smarie/pytest-patterns/issues)

## Running the tests

This project uses `pytest`.

```bash
pytest -v pytest_patterns/tests/
```

You may need to install requirements for setup beforehand, using 

```bash
pip install -r ci_tools/requirements-test.txt
```

## Generating the documentation page

This project uses `mkdocs` to generate its documentation page. Therefore building a local copy of the doc page may be done using:

```bash
mkdocs build -f docs/mkdocs.yml
```

You may need to install requirements for doc beforehand, using 

```bash
pip install -r ci_tools/requirements-doc.txt
```

## Generating the test reports

The following commands generate the html test report and the associated badge. 

```bash
pytest --junitxml=junit.xml -v pytest_patterns/tests/
ant -f ci_tools/generate-junit-html.xml
python ci_tools/generate-junit-badge.py
```

### Merging pull requests with edits - memo

Ax explained in github ('get commandline instructions'):

```bash
git checkout -b <git_name>-<feature_branch> master
git pull https://github.com/<git_name>/pytest-patterns.git <feature_branch> --no-commit --ff-only
```

if the second step does not work, do a normal auto-merge (do not use **rebase**!):

```bash
git pull https://github.com/<git_name>/pytest-patterns.git <feature_branch> --no-commit
```

Finally review the changes, possibly perform some modifications, and commit.
