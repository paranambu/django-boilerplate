{% for _ in cookiecutter.project_name %}*{% endfor %}
{{ cookiecutter.project_name }}
{% for _ in cookiecutter.project_name %}*{% endfor %}

{{ cookiecutter.project_description }}

Getting Started
===============

Prerequisites
-------------

* Python >= 3.6.0 <https://docs.python.org/3/index.html>
* Node >= 8.10.0 <https://nodejs.org/en/docs/>
* Postgres >= 10.0 <https://www.postgresql.org/docs/>
* Redis >= 4.0 <https://redis.io/download>

Installing
----------

1. Create the database and the virtual environment. We recommend using `virtualenvwrapper <http://virtualenvwrapper.readthedocs.io/en/latest/index.html>`_.

2. Create an .env file and set variables. Examples can be found in :code:`.env.example`.

3. Install the environment:

   .. code-block:: bash

      frontend$ npm install
      backend$ pip install -r requirements.txt
      backend$ python manage.py migrate

4. Watch static files:

   .. code-block:: bash

      frontend$ npm start

5. Start the server:

   .. code-block:: bash

      backend$ python manage.py runserver

The site will be available on <http://127.0.0.1:8000>.

Usually the workflow is to start the environment, install dependencies,
run migrations and run the server. Sometimes you will need to activate the
celery service, but it is optional in development.

Deploy
======

TODO

Translations
============

Example of how to make messages for spanish (es):

   .. code-block:: bash

      backend$ django-admin makemessages --locale=es

Example of how to make messages for JS files:

   .. code-block:: bash

      frontend$ npm run makemessages es

Django translations are compiled automatically during the deployment.

If you want to compile messages, use the compilemessages command:

   .. code-block:: bash

      backend$ django-admin compilemessages --locale=es

Tests
=====

   .. code-block:: bash

      backend$ pytest
      frontend$ npm run test

      # example
      backend$ pytest apps/main/tests/test_error_pages.py
      frontend$ npm run test js/utils/__tests__/resetFactorySequences.test.js

The tests lives in a directory inside the same directory of the code being tested.
For example, for python, the tests for :code:`foo/bar.py` lives in :code:`foo/tests/test_bar.py`.
For js, the tests for :code:`foo/bar.js` lives in :code:`foo/__tests__/bar.test.js`.

Useful commands
===============

   .. code-block:: bash

      # To build the image
      $ sudo docker-compose -f docker/docker-compose.web.yml build

      # To run bash inside a container
      $ sudo docker-compose -f docker/docker-compose.web.yml run web bash
