Examples
========

Example apps demonstating usage.

Note: The examples also have tests located in `../tests/examples`,
they are run as part of the main test suite for the whole project.


Examples description
--------------------

minimal_db
^^^^^^^^^^

Minimal example using sqlalchemy.

.. code-block:: text

    FLASK_APP=minimal_db:app flask run

minimal_nodb
^^^^^^^^^^^^

Minimal example without using sqlalchemy or marshmallow-sqlalchmy.

.. code-block:: text

    FLASK_APP=minimal_nodb:app flask run

complete_db
^^^^^^^^^^^

Complete example project using sqlalchemy and marshmallow-sqlalchemy.

.. code-block:: text

    FLASK_APP=complete_db.app flask run
