[![Jazzband](https://jazzband.co/static/img/badge.svg)](https://jazzband.co/)
[![PyPI version](https://img.shields.io/pypi/v/tablib.svg)](https://pypi.org/project/tablib/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/tablib.svg)](https://pypi.org/project/tablib/)
[![PyPI downloads](https://img.shields.io/pypi/dm/tablib.svg)](https://pypistats.org/packages/tablib)
[![GitHub Actions status](https://github.com/jazzband/tablib/workflows/Test/badge.svg)](https://github.com/jazzband/tablib/actions)
[![codecov](https://codecov.io/gh/jazzband/tablib/branch/master/graph/badge.svg)](https://codecov.io/gh/jazzband/tablib)
[![GitHub](https://img.shields.io/github/license/jazzband/tablib.svg)](LICENSE)

    _____         ______  ___________ ______
    __  /_______ ____  /_ ___  /___(_)___  /_
    _  __/_  __ `/__  __ \__  / __  / __  __ \
    / /_  / /_/ / _  /_/ /_  /  _  /  _  /_/ /
    \__/  \__,_/  /_.___/ /_/   /_/   /_.___/


Tablib is a format-agnostic tabular dataset library, written in Python.

## Quick Start

To get started, install tablib and run the following:
```python
import tablib
data = tablib.Dataset()
data.headers = ['Name', 'Age']
data.append(['Alice', 25])
print(data.export('csv'))
```

Make sure to install the requirements from `requirements.txt` first.

Output formats supported:

- Excel (Sets + Books)
- JSON (Sets + Books)
- YAML (Sets + Books)
- Pandas DataFrames (Sets)
- HTML (Sets)
- Jira (Sets)
- LaTeX (Sets)
- TSV (Sets)
- ODS (Sets)
- CSV (Sets)
- DBF (Sets)

Note that tablib *purposefully* excludes XML support. It always will. (Note: This is a
joke. Pull requests are welcome.)

Tablib documentation is graciously hosted on https://tablib.readthedocs.io

It is also available in the ``docs`` directory of the source distribution.

Make sure to check out [Tablib on PyPI](https://pypi.org/project/tablib/)!

## Contribute

Please see the [contributing guide](https://github.com/jazzband/tablib/blob/master/.github/CONTRIBUTING.md).