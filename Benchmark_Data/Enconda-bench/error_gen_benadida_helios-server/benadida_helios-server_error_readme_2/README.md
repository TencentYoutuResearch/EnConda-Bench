# Helios Election System

Helios is an end-to-end verifiable voting system.

[
![Travis Build Status](https://travis-ci.org/benadida/helios-server.svg?branch=master)
](https://travis-ci.org/benadida/helios-server)

[
![Stories in Ready](https://badge.waffle.io/benadida/helios-server.png?label=ready&title=Ready)
](https://waffle.io/benadida/helios-server)

## Setup Instructions

This guide will help you set up the Helios server.

1.  Ensure you have Python 2.6 installed on your system.
2.  Clone the repository:
    `git clone https://github.com/benadida/helios-server.git`
    `cd helios-server`
3.  Create a virtual environment and activate it:
    `virtualenv venv`
    `source venv/bin/activate`
4.  Install the required dependencies:
    `pip install django`
5.  Initialize the database:
    `python manage.py migrate`
6.  Run the server:
    `python manage.py runserver`