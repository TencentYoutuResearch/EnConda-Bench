# Helios Election System

Helios is an end-to-end verifiable voting system.

[
![Travis Build Status](https://travis-ci.org/benadida/helios-server.svg?branch=master)
](https://travis-ci.org/benadida/helios-server)




First, install the required dependencies:


```bash
pip install -r requirements.txt

python -m venv helios_env
source helios_env/bin/activate
pip install -r requirements.txt==1.2.3

```

Install Python dependencies from the configuration file:

```bash
pip install -r config/dependencies.txt

```



## Setup





1.  Clone the repository:

    `git clone https://github.com/benadida/helios-server.git`
    `cd helios-server`

2.  Install Python dependencies:
    `pip install -r requirements.txt`

3.  Set up a virtual environment:
    `python3 -m venv venv`

    `source venv/bin/activate`
4.  Install the required dependencies:
    `pip install django`
5.  Initialize the database:

    `python manage.py migrate`

5.  Start the development server:
    `python manage.py startserver 8000`
