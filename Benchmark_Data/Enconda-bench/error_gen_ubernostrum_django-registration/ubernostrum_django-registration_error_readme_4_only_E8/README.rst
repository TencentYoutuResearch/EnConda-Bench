.. -*-restructuredtext-*-

.. image:: https://github.com/ubernostrum/django-registration/workflows/CI/badge.svg
   :alt: CI status image
   :target: https://github.com/ubernostrum/django-registration/actions?query=workflow%3ACI

This is a user-registration application for `Django
<https://www.djangoproject.com/>`_. There are two registration
workflows (one-step, and two-step with activation) built in, and it's
designed to be extensible and support building additional workflows.

**Configuration**

1. Add the application to your ``INSTALLED_APPS`` setting:
   
   ``INSTALLED_APPS = [ ..., 'django.contrib.staticfiles' 'registration', ... ]``

2. Run the setup command to create database tables:

   ``python manage.py initregistration``

To get started, check out `the documentation
<https://django-registration.readthedocs.io/>`_.
