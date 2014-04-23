Installation
============

Installation is simple, use your favourite PyPi package installer and install
``Flask-Velox``, for example with ``pip``:

.. code-block:: sh

    pip install Flask-Velox

Integration with Flask
----------------------

Next we need to integrate ``Flask-Velox`` into your Flask app, all you need to
do is import the extenstion, insatiate the ``Velox`` class and call
``init_app`` with your application object. A simple example:

.. code-block:: python

    from flask import Flask
    from flask.ext.velox import Velox

    app = Flask(__name__)

    velox = Velox()
    velox.init_app(app)

    app.run()
