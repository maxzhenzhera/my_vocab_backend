****************
My Vocab Backend
****************
| Before: investigate ``.env.example`` and fill ``.env.[prod/dev/test]``.
| Note: for ``prod`` you have to generate local SSL certs and tweak *hosts* for local running (will describe it's later).

Run in Docker
=============
| ``Test`` [tests (pytest), linting (flake8), type-checking (mypy)]:
.. code-block:: bash
    $ make test
| ``Prod`` [Nginx + Gunicorn]:
.. code-block:: bash
    $ make prod
| ``Dev`` [Uvicorn]:
.. code-block:: bash
    $ make dev

| Clean docker stuff:
.. code-block:: bash
    $ make test-down
    $ make prod-down
    $ make dev-down
    $ make clean

Run locally
=============
| Serve **postgres** DB for app. [I'm sure You understand that you have to put **DB URI** to that **DB** in *.env* files.]
| Put ``APP_ENV`` in *.env*./*environment*.

| ``Test``:
.. code-block:: bash
    $ flake8 app
    $ flake8 tests
    $ mypy app
    $ mypy tests --disable-error-code=override --disable-error-code=misc --disable-error-code=no-untyped-def
    $ pytest
| ``Prod``:
.. code-block:: bash
    $ python app/__main__.py
| ``Dev``:
.. code-block:: bash
    $ python app/__main__.py

| ``Prod`` and ``Dev`` runners depend on ``APP_ENV`` variable.

Full Prod setup
===============
| Install `mkcert <https://github.com/FiloSottile/mkcert>`_.
.. code-block:: bash
    $ mkcert backend.myvocab.com localhost 127.0.0.1 ::1
| Put this cert under *./nginx/certs*. [Use other domains? Substitute all occurrences]
| Link cert to nginx conf.d (for local running):
.. code-block:: bash
    $ cd /etc/nginx/conf.d
    $ ln -s <path-to-cert> .
    $ ln -s <path-to-cert-key> .
| Tweak */etc/hosts* file:
.. code-block:: bash
    ...
    # custom domains
    127.0.0.1       gunicorn_host
    127.0.0.1       backend.myvocab.com

| You're ready to run both locally as in Docker.
| Serve **nginx** for local running.

Afterwords
==========
``noli esse irrumatus - pone stellam.``