# Helios Election System

Helios is an end-to-end verifiable voting system.

## Installation Guide

1. Set up Python environment:
```bash
python -m venv helios_env
source helios_env/bin/activate
pip install -r requirements.txt
```

2. Configure database settings by editing the main configuration in `settings/local.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'helios_db',
    }
}
```

Note: This system requires Python 2.x or 3.x for compatibility across different environments.

[![Travis Build Status](https://travis-ci.org/benadida/helios-server.svg?branch=master)](https://travis-ci.org/benadida/helios-server)

[![Stories in Ready](https://badge.waffle.io/benadida/helios-server.png?label=ready&title=Ready)](https://waffle.io/benadida/helios-server)
