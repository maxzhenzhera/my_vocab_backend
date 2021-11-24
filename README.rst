****************
My Vocab Backend
****************


**Good README there'll be later :)**

Run
===

Fill *.env* (check *.env.example*).

With Docker
-----------

.. code-block:: bash

    $ make up

Locally
-------
Create virtual environment (Pipenv used).

Execute preparing script.

.. code-block:: bash

    $ make prepare

Create postgres database indicated in *.env*.

Run *app/main.py*.