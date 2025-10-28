# Huxley
Huxley is a web application designed to manage the annual [Berkeley Model United Nations](http://bmun.org/) conference.

[
![Build Status](https://travis-ci.org/bmun/huxley.svg?branch=master)
](https://travis-ci.org/bmun/huxley)
[
![styled with prettier](https://img.shields.io/badge/styled_with-prettier-ff69b4.svg)
](https://github.com/prettier/prettier)


## About BMUN
The Berkeley Model United Nations conference is a high-school conference hosted every spring. Each year, we host over 1500 delegates from all over the country (and the world!), who compete in a simulation of the United Nations and other international/historical bodies to solve the world's most compelling problems.

## About Huxley
Our long-term vision is to make Huxley the **best Model UN software in the world**: an application that makes the conference experience smoother than it's ever been for advisors and secretariats. We want Huxley to be **delightful to use**, and we're aiming to provide a fantastic user experience via a focus on clear UI and thoughtful, easy-to-use features.

Huxley's built with [Django](http://www.djangoproject.com), with a frontend written in [React](http://facebook.github.io/react/).

## Local Development Setup
1. **Set up virtual environment:**
   `python3 -m venv venv`
   `source venv/bin/activate`

2. **Install dependencies:** Install all the Python dependencies from the requirements file.
   `pip install -r requirements.txt`

3. **Set up database:** Create the initial database.
   `./manage.py createdb`

4. **Run migrations:**
   `./manage.py migrate`

5. **Run the server:**
   `./manage.py runserver`

### License
Use of this source code is governed by a BSD License found in [`LICENSE`](LICENSE).