=============================
Admin/Developer Documentation
=============================

.. contents::


Getting started
===============

You need to be able to run Docker.

Git clone and then run::

   $ make build
   $ make run

Now a development server should be available at
``http://localhost:8000``.

To test the symbolication run::

   $ curl -d '{"stacks":[[[0,11723767],[1, 65802]]],"memoryMap":[["xul.pdb","44E4EC8C2F41492B9369D6B9A059577C2"],["wntdll.pdb","D74F79EB1F8D4A45ABCD2F476CCABACC2"]],"version":4}' http://localhost:8000/symbolicate/v5

Development services
====================

What's Deployed
---------------

Check out https://whatsdeployed.io/s-5HY

Datadog
-------

If you have access to a Mozilla Cloud Ops Datadog account, use this to
consume the metrics Tecken sends via ``statsd``. One is for staying
health, the other is for keeping track how it does things.

`Tecken dashboards <https://app.datadoghq.com/dashboard/lists?q=tecken>`_

Sentry
------

Prod: https://sentry.prod.mozaws.net/operations/symbols-prod/

Stage: https://sentry.prod.mozaws.net/operations/symbols-stage/

Dev: https://sentry.prod.mozaws.net/operations/symbols-dev/

Frontend: https://sentry.prod.mozaws.net/operations/symbols-frontend/

Code Conventions
================

All code files need to start with the MPLv2 header::

    # This Source Code Form is subject to the terms of the Mozilla Public
    # License, v. 2.0. If a copy of the MPL was not distributed with this
    # file, You can obtain one at http://mozilla.org/MPL/2.0/.

To check if any file is lacking a license preamble, run:

.. code-block:: shell

    $ ./bin/sanspreamble.sh

It will exit non-zero if there are files lacking the preamble. It only
checks git checked in files.

PEP8 is nice. All files are expected to be PEP8 and pyflakes compliant
and the PEP8 rules (and exceptions) are defined in ``.flake8`` under
the ``[flake8]`` heading.

If you hit issues, instead of re-writing the rules consider
appending a comment on the end of the line that says ``# noqa``.

All Python code is and should be formatted with `black <https://github.com/ambv/black>`_.

Google Cloud Platform Setup
===========================

First, you need to set up a project.

1. log into your `Google Cloud Platform console <https://console.cloud.google.com/>`_
2. create a project

Then you need to create a service account and generate a JSON key file.

1. in the project, go to "IAM & admin" and then "Service accounts" and click on
   "CREATE SERVICE ACCOUNT"
2. name it something useful
3. give it the "Storage Admin" role
4. click on "CONTINUE"
5. click on "CREATE KEY", generate a JSON file, and download it
6. click on "DONE"
7. rename the JSON file as ``google_service_account.json`` and put it into the
   Tecken project root directory

.. Note::

   You can name the JSON file something else. If you do, set the ``GOOGLE_APPLICATION_CREDENTIALS``
   key in your ``.env`` file with the file name.

Then you need to create a Google Cloud Storage bucket.

1. in the project, go to "Storage"
2. click on "CREATE BUCKET"
3. name it something like "tecken-dev-bucket"
4. click on "Permissions" tab
5. click on "Add member" button, type in the full service account email address, and then
   add the "Storage admin" role
6. set the ``DJANGO_SYMBOL_URLS`` and ``DJANGO_UPLOAD_DEFAULT_URL`` variables
   in your ``.env`` file:

   .. code-block:: shell

       DJANGO_SYMBOL_URLS=https://storage.googleapis.com/my-gcs-bucket
       DJANGO_UPLOAD_DEFAULT_URL=https://storage.googleapis.com/my-gcs-bucket

Give the service account access to the bucket.

1. In the project, go to "Storage"
2. click on the bucket
3. click on the "Permissions" tab
4. click on "Add members" button
5. paste in the entire service account address and add "Storage admin" role

Once all that's done, then everything should be set. The configuration settings
are checked when you start the Tecken server.

Google Cloud Storage Bucket Configuration
=========================================

Tecken will *not* attempt to correct or even check *how* your Google Cloud
Storage buckets are configured. For example, to simulate production mode
you might want to set a life-cycle configuration to delete symbols older
than one year.

A more important example, you might want to make your bucket, by default,
is to make it publicly available. Meaning, files uploaded should
be reachable, via HTTP, without authentication. You can make these
kinds of configurations by installing the ``gsutil`` tool
(e.g. ``brew install gsutil`` and ``gsutil config``).
Suppose your bucket is called ``my-gcs-bucket`` you can make it
public by default with:

.. code-block:: shell

    $ gsutil defacl set public-read gs://my-gcs-bucket


Documentation
=============

Documentation is compiled with Sphinx_ and is available on ReadTheDocs.
API is automatically extracted from docstrings in the code.

To build the docs, run this:

.. code-block:: shell

    $ make docs

This is the same as running:

.. code-block:: shell

    $ ./bin/build-docs-locally.sh

To iterate on writing docs and testing that what you type compiles correctly,
run the above mentioned command on every save and then open the file
``docs/_build/html/index.html``. E.g.

.. code-block:: shell

    # the 'open' command is for OSX
    $ open docs/_build/html/index.html


.. _Sphinx: http://www.sphinx-doc.org/en/stable/

Hyperactive Document Writing
============================

If you write a lot and want to see the changes much sooner after having
written them, you can temporarily enter a shell and run exactly the
minimum needed. First start a shell and install the Python requirements:

.. code-block:: shell

   $ make test
   > pip install -r docs-requirements.txt

Now, you can run the command manually with just...:

.. code-block:: shell

   > make -C docs html

And keep an browser open to the file ``docs/_build/html/index.html`` in
the host environment.

If you're really eager to have docs built as soon as you save the ``.rst``
file in your editor, run this command:

.. code-block:: shell

   > watchmedo shell-command -W -c 'make -C docs html' -R .

Note that if you make a change/save *during* the build, it will ignore that.
So wait until it has finished before you save again. Note, that the ``.rst``
file you're working on doesn't actually need to change. A save-file is enough.

Also note that it won't build the docs until there has been at least one
file save.

Testing
=======

To run the tests, run this:

.. code-block:: shell

   $ make test


Tests go in ``tests/``. Data required by tests goes in ``tests/data/``.

If you need to run specific tests or pass in different arguments, you can run
bash in the base container and then run ``py.test`` with whatever args you
want. For example:

.. code-block:: shell

   $ make shell
   > py.test

   <pytest output>

   > py.test tests/test_symbolicate.py


We're using py.test_ for a test harness and test discovery.

.. _py.test: http://pytest.org/


Hyperactive Test Running
========================

If you want to make tests run as soon as you save a file you have to
enter a shell and run ``ptw`` which is a Python package that is
automatically installed when you enter the shell. For example:

.. code-block:: shell

   $ make shell
   > ptw

That will re-run ``py.test`` as soon as any of the files change.
If you want to pass any other regular options to ``py.test`` you can
after ``--`` like this:

.. code-block:: shell

  $ make shell
  > ptw -- -x --other-option


Managing Python Requirements
============================

All Python requirements needed for development and production needs to be
listed in ``requirements.txt`` with sha256 hashes.

The most convenient way to modify this is to run ``hashin`` in a shell.
For example:

.. code-block:: shell

   $ make shell
   > pip install hashin
   > hashin Django==1.10.99
   > hashin other-new-package

This will automatically update your ``requirements.txt`` but it won't
install the new packages. To do that, you need to exit the shell and run:

.. code-block:: shell

   $ make build


To check which Python packages are outdated, use `piprot`_ in a shell:

.. code-block:: shell

   $ make shell
   > pip install piprot
   > piprot -o

The ``-o`` flag means it only lists requirements that are *out of date*.

.. note:: A good idea is to install ``hashin`` and ``piprot`` globally
   on your computer instead. It doesn't require a virtual environment if
   you use `pipsi`_.

.. _piprot: https://github.com/sesh/piprot
.. _pipsi: https://github.com/mitsuhiko/pipsi

Running ``gunicorn`` locally
============================

To run ``gunicorn`` locally, which has concurrency, run:

.. code-block:: shell

   $ make gunicorn

You might want to temporarily edit ``.env`` and set ``DJANGO_DEBUG=False``
to run it in a more production realistic way.

Integration Testing
===================

tecken-loader
-------------

Use `tecken-loader`_ for integration testing uploading, downloading,
and symbolication APIs. It contains a series of scripts and molotov
loadtests.

Details at `mozilla-services/tecken-loader
<https://github.com/mozilla-services/tecken-loader>`_.

This is useful for sending somewhat realistic symbolication requests
that reference symbols that are often slightly different.


webapp
------

Here's a rough webapp test script:

1. go to website
2. wait for front page to load
3. log in
4. click on "downloads" in navbar
5. click on "user management" in navbar
6. click on "API tokens" in navbar
7. click on "uploads" in navbar
8. click on "symbolication" in navbar
9. click on "help" in navbar

Prod-like running locally
=========================

First you need to start Tecken with a set of configurations that
mimics what's required in prod, except we're doing this in docker.

To do that, you need to set ``DJANGO_CONFIGURATION=Prodlike`` and
run the gunicorn workers:

.. code-block:: shell

    $ docker-compose run --service-ports --user 0  web bash

This will start 4 ``gunicorn`` workers exposed on ``0.0.0.0:8000`` and
exposed outside of docker onto your host.

.. note:: If this fails to start, some exceptions might be hidden. If so,
          start a shell ``docker-compose run --user 0 web bash`` and run:
          ``DJANGO_UPLOAD_DEFAULT_URL=http://minio:9000/testbucket DJANGO_SYMBOL_URLS=http://minio:9000/testbucket DJANGO_CONFIGURATION=Prodlike gunicorn tecken.wsgi:application -b 0.0.0.0:8000 --workers 4 --access-logfile -``

That configuration **forces** you to run with ``DEBUG=False`` independent
of what value you have set in ``.env`` for ``DEBUG``. Thus making it easy
to switch from regular debug-mode development to prod-like serving.

The second step for this to be testable is to reach the server with ``HTTPS``
or else the app will forcibly redirect you to the ``https://`` equivalent of
whatever URL you attempt to use (e.g. ``http://localhost:8000/`` redirects
to ``https://localhost:8000/``)

To test this, run a local Nginx server. But first, create a suitable
hostname. For example, ``prod.tecken.dev``. Edit ``/etc/hosts`` and enter
a line like this::

    127.0.0.1       prod.tecken.dev

To generate an nginx config file, run ``./test-with-nginx/generate.py``.
That will be print out a Nginx configuration file you can put where
you normally put Nginx configuration files. For example:

.. code-block:: shell

    $ ./test-with-nginx/generate.py --help
    $ ./test-with-nginx/generate.py > /etc/nginx/sites-enabled/tecken.conf
    $ # however you reload nginx


Frontend and prod-like running locally
======================================

When Tecken is deployed with continuous integration, it builds the static
assets files for production use. These files are served by Django using
Whitenoise. Basically, anything that isn't a matched Django URL-to-view
gets served as a static file, if matched.

Suppose you want to run the prod-like frontend locally. For example, you
might be hunting a frontend bug that only happens when the assets are
minified and compiled. To do that you have to manually build the static assets:

.. code-block:: shell

    $ cd frontend
    $ yarn
    $ yarn run build

This should create ``frontend/build/*`` files. For example
``static/js/main.6d3b4de8.js``. This should now be available *thru* Django
at ``http://localhost:8000/static/js.main.6d3b4de8.js``.

When you're done you can delete ``frontend/build`` and
``frontend/node_modules``.

Running things in background vs foreground
==========================================

By default ``make run`` is wired to start three things in the foreground:

* Django (aka. ``web``)

* Celery (aka. ``worker``)

* React dev server (aka. ``frontend``)

This is done by running ``docker-compose up web worker frontend``. These
services' output is streamed together to stdout in the foreground that
this ``docker-compose up ...`` runs.

All other things that these depend on are run in the background. Meaning
you don't see, for example, what the ``minio`` service does. It knows to
*start* because in ``docker-compose.yml`` ``web`` is **linked** to
``minio``.

If you instead want to run, for example, ``minio`` in the foreground here's
how:

1. Comment out ``minio`` from the ``links`` part of ``web`` in ``docker-compose.yml``

2. In a terminal run ``docker-compose up minio``.

3. In another terminal run ``make run``

Alternatively, just do step 1, from the list above, and then run:
``docker-compose up minio web worker frontend``.


All metrics keys
================

To get insight into all metrics keys that are used, a special Markus backend
is enabled called ``tecken.markus_extra.LogAllMetricsKeys``. It's enabled
by default in local development. And to inspect its content you can either
open ``all-metrics-keys.json`` directly (it's git ignored) or you can run:

.. code-block:: shell

    $ make shell
    $ ./bin/list-all-metrics-keys.py

Now you can see a list of all keys that are used. Take this and, for example,
make sure you make a graph in Datadog of each and everyone. If there's a key
in there that you know you don't need or care about in Datadog, then delete
it from the code.

The file ``all-metrics-keys.json`` can be deleted any time and it will be
recreated again.


Celery in local development mode
================================

When you do something like ``make run`` it starts Django, the frontend
and the Celery worker. But it's important to note that it starts Celery
with ``--purge``. That means that every time you start up the worker,
all jobs that have been previously added to the Celery query are purged.

This is to prevent foot-shooting. Perhaps a rogue unit test that didn't mock
the broker and accidentally added hundreds of jobs that all fail.
Or perhaps you're working on a git branch that changes how the worker job
works and as you're jumping between git branches you start and stop the worker
so that the wrong jobs are sent using the wrong branch.

Another real thing that can happen is that when you're doing loadtesting of
the web app, and only run that in docker, but since the web app writes to
the same Redis (the broker) thousands of jobs might be written that never
get a chance to be consumed by the worker.

This is why ``docker-compose`` starts ``worker-purge`` instead of ``worker``
which is the same thing except it's started with ``--purge`` and this should
only ever be done on local docker development.


Minio (S3 mock server)
======================

When doing local development we, by default, mock AWS S3 and instead use
`minio`_. It's API compatible so it should reflect how AWS S3 works but
with the advantage that you don't need an Internet connection and real
S3 credentials just to test symbol uploads for example.

When started with docker, it starts a web server on ``:9000`` that you can
use to browse uploaded files. Go to ``http://localhost:9000``.

.. _`minio`: https://minio.io/


How to Memory Profile Python
============================

The trick is to install https://pypi.python.org/pypi/memory_profiler
(and ``psutil``) and then start Gunicorn with it. First start a
shell and install it there:

.. code-block:: shell

    $ docker-compose run --service-ports --user 0  web bash
    # pip install memory_profiler psutil

Now, to see memory reports of running functions, add some code to the
relevant functions you want to memory profile:

.. code-block:: python


    from memory_profiler import profile

    @profile
    def some_view(request):
        ...

Now run Gunicorn:

.. code-block:: shell

    $ python -m memory_profiler  `which gunicorn` tecken.wsgi:application -b 0.0.0.0:8000 --timeout 60 --workers 1 --access-logfile -


How to do local Upload by Download URL
======================================

When doing local development and you want to work on doing Symbol Upload
by HTTP posting the URL, you have a choice. Either put files somewhere
on a public network, or serve the locally.

Before we start doing local Upload By Download URL, you need to make your
instance less secure since you'll be using URLs like ``http://localhost:9090``.
Add ``DJANGO_ALLOW_UPLOAD_BY_ANY_DOMAIN=True`` to your ``.env`` file.

To serve them locally, first start the dev server (``make run``). Then
you need to start a bash shell in the current running web container:

.. code-block:: shell

    $ make currentshell

Now, you need some ``.zip`` files in the root of the project since it's
mounted and can be seen by the containers. Once they're there, start a
simple Python server:

.. code-block:: shell

    $ ls -lh *.zip
    $ python -m http.server --bind 0.0.0.0 9090

Now, you can send these in with ``tecken-loadtest`` like this:

.. code-block:: shell

    $ export AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxx
    $ python upload-symbol-zips.py http://localhost:8000 -t 160 --download-url=http://localhost:9090/symbols.zip

This way you'll have 3 terminals. 2 bash terminals inside the container
and one outside in the ``tecke-loadtests`` directory on your host.


Frontend linting - Prettier files
=================================

All ``.js`` files in the frontend code is expected to be formatted with
`Prettier`_. Ideally your editor should be configured to automatically
apply ``Prettier`` on save. Or by a git hook.

If you forget to format any files in a Pull Request, a linting check in
CircleCI will fail if any file hasn't been formatted. To test this locally,
use:

.. code-block:: shell

    $ docker-compose run frontend lint

If you get any output, it means it found files that should/could have been
formatted. The error message will explain what files need attention and
how to just format them all right now.

If you don't really care all that much about what the difference is and
just want to fix it automatically run:

.. code-block:: shell

    $ docker-compose run frontend lintfix

.. _`Prettier`: https://prettier.io/


Python warnings
===============

The best way to get **all** Python warnings out on ``stdout`` is to run
Django with the ``PYTHONWARNINGS`` environment variable.

.. code-block:: shell

    $ docker-compose run --service-ports --user 0  web bash

Then when you're in bash of the web container:

.. code-block:: shell

    # PYTHONWARNINGS=d ./manage.py runserver 0.0.0.0:8000

How to ``psql``
===============

The simplest way is to use the shortcut in the ``Makefile``

.. code-block:: shell

    $ make psql

If you have a ``.sql`` file you want to send into ``psql`` you can do that
too with:

.. code-block:: shell

    $ docker-compose run db psql -h db -U postgres < stats-queries.sql

...for example.


Backup and Restore PostgreSQL
=============================

To make a backup of the whole database use ``pg_dump`` like this:

.. code-block:: shell

    $ docker-compose run db pg_dump -h db -U postgres > tecken.sql

If you import it with:

.. code-block:: shell

    $ docker-compose run db psql -h db -U postgres < tecken.sql


Enable full logging of SQL used
===============================

To see all the SQL the ORM uses, change the ``LOGGING`` configuration
in ``settings.py``.

First, change the level for ``django.db.backends`` from ``INFO`` to ``DEBUG``.
Second, change ``LOGGING_DEFAULT_LEVEL`` from ``INFO`` to ``DEBUG``.

Now, when you run ``make run`` you should see all SQL from Django into
the terminal stdout.


Auth not working
================

There are many reasons for why authentication might not work. Most of the
pit falls lies with the the configuration and credentials around OpenID
Connect. I.e. Auth0 in our current case.

Another important thing is that on the Django side, caching and cookies work.

If you have trouble authenticating you can start the server and go to:
``http://localhost:8000/__auth_debug__``.  It will check that the cache
can work between requests and that session cookies can be set and read.


How to make a Zip file
======================

Suppose you have a file like ``libxul.so.sym``. Suppose also that you have
multiple files you want to put into the zip, but for now we'll just make
a zip of one file but use the ``-r`` flag to demonstrate how to do it
if there were multiple files:

.. code-block:: shell

    $ mkdir zipthis
    $ mkdir zipthis/libxul.so
    $ mkdir zipthis/libxul.so/13E87871A778CDBAF11B298FD05E2DBA0
    $ cp libxul.so.sym zipthis/libxul.so/13E87871A778CDBAF11B298FD05E2DBA0/
    $ cd zipthis
    $ zip mysymbols -r *
    $ ls -l mysymbols.zip
    -rw-r--r--  1 peterbe  staff  40945250 Aug 10 14:54 mysymbols.zip


How to make a Zip file from downloading
=======================================

The above section was about how to create a valid symbol zip file using
basic UNIX/bash tools. Another, more convenient, way is to use the
script ``bin/make-a-zip.py``. You specify the names of symbols from
``https://symbols.mozilla.org``, by default, and it downloads them and
packages it up in the right way. This is useful if you want to reproduce
a problem with a symbol file locally for example. E.g.

.. code-block:: shell

    $ ./bin/make-a-zip.py --help
    $ ./bin/make-a-zip.py qipcap.pdb/54EB115B9E735A17A87BCA540732CE171 fake.dll/5C34D92C63000/fake.dl_
    Downloaded 3670 bytes (3.6KB, 10.6KB on disk) into /tmp/tmpti3fksrr/qipcap.pdb/54EB115B9E735A17A87BCA540732CE171
    Downloaded 199535 bytes (194.9KB, 194.9KB on disk) into /tmp/tmpti3fksrr/fake.dll/5C34D92C63000
    Wrote /Users/peterbe/Desktop/symbols.zip

Note that if you omit the filename of the symbol file, it assumes
``modulename + .sym``.
E.g. ``qipcap.pdb/54EB115B9E735A17A87BCA540732CE171/qipcap.sym``.


``black``
=========

`black <https://github.com/ambv/black>`_. is the Python code formatting tool we use
to format all non-generated Python code. In CI, we test that all code passes
``black --diff --check ...``. When doing local development, consider setting
up either some sort of "format on save" in your editor or a git pre-commit hook.

To check that all code is formatted correctly, run:

.. code-block:: shell

    $ docker-compose run linting lintcheck

If you have a bunch of formatting complaints you can automatically fix them all with:

.. code-block:: shell

    $ docker-compose run linting blackfix


Debugging ``minio`` container
=============================

``minio`` is used in ``docker-compose`` as a local substitute for AWS S3.
If it fails to start, it could be because of an upgrade of the image on
Dockerhub. If it fails to start, try first to run:

.. code-block:: shell

    $ docker-compose build minio
    $ docker-compose up minio

If you get an error that looks like this:

    You are running an older version of Minio released 7 months ago

The simplest solution is to delete the ``miniodata`` directory. E.g:

.. code-block:: shell

    $ rm -fr miniodata


Debugging a "broken" Redis
==========================

By default, we have our Redis Cache configured to swallow all exceptions
(...and just log them). This is useful because the Redis Cache is only
supposed to make things faster. It shouldn't block things from working even
if that comes at a price of working slower.

To simulate that Redis is "struggling" you can use the
`CLIENT PAUSE <https://redis.io/commands/client-pause>`_ command. For example:

.. code-block:: shell

    $ make redis-cache-cli
    redis-cache:6379> client pause 30000
    OK

Now, for 30 seconds (30,000 milliseconds) all attempts to talk to Redis Cache
is going to cause a ``redis.exceptions.TimeoutError: Timeout reading from socket``
exception which gets swallowed and logged. But you *should* be able to use
the service fully.

For example, all things related to authentication, such as your session cookie
should continue to work because we use the ``cached_db`` backend in
``settings.SESSION_ENGINE``. It just means we have to rely on PostgreSQL to
verify the session cookie value on each and every request.


Giving users upload permission
==============================

The user should write up a bug. See :ref:`upload-basics`.

If the user is a Mozilla employee, needinfo the user's manager and verify the
user needs upload permission.

If the user is not a Mozilla employee, find someone to vouch for the user.

Once vouched:

1. Log in to `<https://symbols.mozilla.org/users>`_
2. Use the search filter at the bottom of the page to find the user
3. Click to edit and make give them the "Uploaders" group (only).
4. Respond and say that they now have permission and should be able to either
   upload via the web or create an API Token with the "Upload Symbol Files"
   permission.
5. Resolve the bug.
