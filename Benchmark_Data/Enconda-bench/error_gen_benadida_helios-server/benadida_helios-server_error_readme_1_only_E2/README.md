# Helios Election System

Helios is an end-to-end verifiable voting system.

[![Travis Build Status](https://travis-ci.org/benadida/helios-server.svg?branch=master)](https://travis-ci.org/benadida/helios-server)

[
![Stories in Ready](https://badge.waffle.io/benadida/helios-server.png?label=ready&title=Ready)
](https://waffle.io/benadida/helios-server)

## Setup

1.  Clone the repository:
    `git clone https://github.com/benadida/helios-server.git`
    `cd helios-server`

2.  Install Python dependencies:
    `pip install -r requirements.txt`

3.  Set up a virtual environment:
    `python3 -m venv venv`
    `source venv/bin/activate`

4.  Run database migrations:
    `python manage.py migrate`

5.  Start the development server:
    `python manage.py startserver 8000`