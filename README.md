robust
======

[![](https://dev.azure.com/lycantropos/robust/_apis/build/status/lycantropos.robust?branchName=master)](https://dev.azure.com/lycantropos/robust/_build/latest?definitionId=17&branchName=master "Azure Pipelines")
[![](https://readthedocs.org/projects/shewchuk/badge/?version=latest)](https://shewchuk.readthedocs.io/en/latest "Documentation")
[![](https://codecov.io/gh/lycantropos/robust/branch/master/graph/badge.svg)](https://codecov.io/gh/lycantropos/robust "Codecov")
[![](https://img.shields.io/github/license/lycantropos/robust.svg)](https://github.com/lycantropos/robust/blob/master/LICENSE "License")
[![](https://badge.fury.io/py/robust.svg)](https://badge.fury.io/py/robust "PyPI")

In what follows `python` is an alias for `python3.5` or `pypy3.5`
or any later version (`python3.6`, `pypy3.6` and so on).

Installation
------------

Install the latest `pip` & `setuptools` packages versions
```bash
python -m pip install --upgrade pip setuptools
```

### User

Download and install the latest stable version from `PyPI` repository:
```bash
python -m pip install --upgrade robust
```

### Developer

Download the latest version from `GitHub` repository
```bash
git clone https://github.com/lycantropos/robust.git
cd robust
```

Install
```bash
python setup.py install
```

Usage
-----
```python
>>> from robust import cocircular
>>> cocircular.determinant((0, 0), (2, 0), (0, 2), (1, 1))
8
>>> cocircular.determinant((0, 0), (2, 0), (0, 2), (3, 3))
-24
>>> cocircular.determinant((0, 0), (2, 0), (2, 2), (0, 2))
0
>>> from robust import parallelogram
>>> parallelogram.signed_area((0, 0), (2, 0), (0, 0), (0, 2))
4
>>> parallelogram.signed_area((0, 0), (0, 2), (0, 0), (2, 0))
-4
>>> parallelogram.signed_area((0, 0), (0, 2), (0, 0), (0, 2))
0
>>> from robust import projection
>>> projection.signed_length((0, 0), (2, 0), (0, 0), (2, 0))
4
>>> projection.signed_length((0, 0), (2, 0), (0, 0), (-2, 0))
-4
>>> projection.signed_length((0, 0), (2, 0), (0, 0), (0, 2))
0
>>> from robust.angular import Orientation, orientation
>>> orientation((0, 1), (0, 0), (1, 0)) is Orientation.CLOCKWISE
True
>>> orientation((1, 0), (0, 0), (2, 0)) is Orientation.COLLINEAR
True
>>> orientation((1, 0), (0, 0), (0, 1)) is Orientation.COUNTERCLOCKWISE
True
>>> from robust.angular import Kind, kind
>>> kind((0, 0), (1, 0), (2, 0)) is Kind.OBTUSE
True
>>> kind((0, 1), (0, 0), (1, 0)) is Kind.RIGHT
True
>>> kind((1, 0), (0, 0), (2, 0)) is Kind.ACUTE
True
>>> from robust.linear import SegmentsRelationship, segments_relationship
>>> segments_relationship(((0, 0), (1, 0)),
...                       ((2, 0), (3, 0))) is SegmentsRelationship.NONE
True
>>> segments_relationship(((0, 0), (1, 0)),
...                       ((1, 0), (2, 0))) is SegmentsRelationship.TOUCH
True
>>> segments_relationship(((0, 0), (1, 1)),
...                       ((0, 1), (1, 0))) is SegmentsRelationship.CROSS
True
>>> segments_relationship(((0, 0), (1, 0)),
...                       ((0, 0), (1, 0))) is SegmentsRelationship.OVERLAP
True

```

Development
-----------

### Bumping version

#### Preparation

Install
[bump2version](https://github.com/c4urself/bump2version#installation).

#### Pre-release

Choose which version number category to bump following [semver
specification](http://semver.org/).

Test bumping version
```bash
bump2version --dry-run --verbose $CATEGORY
```

where `$CATEGORY` is the target version number category name, possible
values are `patch`/`minor`/`major`.

Bump version
```bash
bump2version --verbose $CATEGORY
```

This will set version to `major.minor.patch-alpha`. 

#### Release

Test bumping version
```bash
bump2version --dry-run --verbose release
```

Bump version
```bash
bump2version --verbose release
```

This will set version to `major.minor.patch`.

### Running tests

Install dependencies
```bash
python -m pip install --force-reinstall -r requirements-tests.txt
```

Plain
```bash
pytest
```

Inside `Docker` container:
- with `CPython`
  ```bash
  docker-compose --file docker-compose.cpython.yml up
  ```
- with `PyPy`
  ```bash
  docker-compose --file docker-compose.pypy.yml up
  ```

`Bash` script (e.g. can be used in `Git` hooks):
- with `CPython`
  ```bash
  ./run-tests.sh
  ```
  or
  ```bash
  ./run-tests.sh cpython
  ```

- with `PyPy`
  ```bash
  ./run-tests.sh pypy
  ```

`PowerShell` script (e.g. can be used in `Git` hooks):
- with `CPython`
  ```powershell
  .\run-tests.ps1
  ```
  or
  ```powershell
  .\run-tests.ps1 cpython
  ```
- with `PyPy`
  ```powershell
  .\run-tests.ps1 pypy
  ```
