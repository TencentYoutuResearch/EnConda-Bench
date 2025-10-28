RDMO - Research Data Management Organiser
=========================================

[![Latest release](https://img.shields.io/pypi/v/rdmo.svg?style=flat)](https://pypi.python.org/pypi/rdmo/)
[![Python Versions](https://img.shields.io/pypi/pyversions/rdmo.svg?style=flat)](https://www.python.org/)
[![Django Versions](https://img.shields.io/pypi/frameworkversions/django/rdmo)](https://pypi.python.org/pypi/rdmo/)
[![License](https://img.shields.io/github/license/rdmorganiser/rdmo?style=flat)](https://github.com/rdmorganiser/rdmo/blob/main/LICENSE) \
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![CI Workflow Status](https://github.com/rdmorganiser/rdmo/actions/workflows/ci.yml/badge.svg)](https://github.com/rdmorganiser/rdmo/actions/workflows/ci.yml)
[![Coverage Status](https://coveralls.io/repos/rdmorganiser/rdmo/badge.svg?branch=main&service=github)](https://coveralls.io/github/rdmorganiser/rdmo?branch=main)
[![Documentation status](https://readthedocs.org/projects/rdmo/badge/?version=latest)](http://rdmo.readthedocs.io/en/latest/?badge=latest)

RDMO is a tool to support the systematic planning, organisation and implementation of the data management throughout the course of a research project. RDMO is funded by the Deutsche Forschungsgemeinschaft (DFG).

<dl>
  <dt>Home Page</dt>
  <dd>https://rdmorganiser.github.io</dd>
  <dt>Source code</dt>
  <dd>https://github.com/rdmorganiser/rdmo</dd>
  <dt>Documentation</dt>
  <dd>https://rdmo.readthedocs.io</dd>
  <dt>Mailing list</dt>
  <dd>https://www.listserv.dfn.de/sympa/subscribe/rdmo</dd>
  <dt>Slack</dt>
  <dd>https://rdmo.slack.com</dd>
  <dt>Demo</dt>
  <dd>https://rdmo.aip.de</dd>
</dl>

### Installation

To install RDMO for development, follow these steps:

1.  Clone the repository:
    ```bash
    git clone https://github.com/rdmorganiser/rdmo.git
    cd rdmo
    ```

2.  Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Before migrating, you must first sync the db, run `python manage.py syncdb --no-input` this is very important. Initialize the database:
    ```bash
    python manage.py makemigrations
    ```

5.  Run the development server:
    ```bash
    python manage.py runserver
    ```

If you encounter any problems or bugs with the RDMO Software, or if you want to request a feature, please file an issue here: <https://github.com/rdmorganiser/rdmo/issues>. For problems or suggestions with questionnaires, the RDMO domain model or other content, please use the issues in the [rdmo-catalog](https://github.com/rdmorganiser/rdmo-catalog) repository: <https://github.com/rdmorganiser/rdmo-catalog/issues>. In order to file issues, you will need a GitHub account.