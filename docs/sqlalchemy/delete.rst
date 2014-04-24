Delete
======

So we can create and update objects but what about deleting them, well we can
do that too with ``Flask-Velox``.

.. note::
    The following packages must be installed:

    * ``Flask-SQLAlchemy``

.. _delete-view:

Delete View
-----------

Deleting a single object is the most basic form of deletion. Implement a view
as follows:

.. seealso::

    * :py:class:`flask_velox.mixins.sqla.delete.DeleteObjectMixin`

The view sends the following context to the template:

* ``model``: The SQLAlchemy model
* ``object``: The object to delete

.. code-block:: python

    from flask.ext.velox.views.sqla.delete import DeleteObjectView
    from yourapp import db
    from yourapp.models import MyModel

    class MyView(DeleteObjectView):
        model = MyModel
        session = db.session
        template = 'delete.html'

.. _delete-view-confirm:

Confirm or not to Confirm
~~~~~~~~~~~~~~~~~~~~~~~~~

In most cases you will want to render a confirm dialog to the user before
actually deleting an object from the database. By default the Delete View will
not delete your object unless a ``confirm`` query parameter is found in the
url. You can disable this behaviour so the object is deleted straight away
without a confirm dialog by setting the ``confirm`` attribute on your view to
``False``:

.. code-block:: python

    class MyView(DeleteObjectView):
        model = MyModel
        session = db.session
        confirm = False

.. _delete-view-example-template:

Example Template
~~~~~~~~~~~~~~~~

As with other views you need to render the confirm dialog yourself so here is
an example to get you going:

.. code-block:: html+jinja

    <p>Are you sure?</p>
    <p>{{ object }}</p>
    <a href="{{ url_for(request.url_rule.endpoint, confirm=True) }}">Do it!</a>

The above template will render a confirm dialog with a link using the current
endpoint with an extra argument so ``?confirm=True`` is appended to the url.

.. _multi-delete-view:

Multi Delete View
-----------------

You may also want the ability to delete mulitple objects, this is achived by
posting a list of ids of ovbjects to delete to the view.

.. seealso::

    * :py:class:`flask_velox.mixins.sqla.delete.MultiDeleteObjectMixin`

.. code-block:: python

    from flask.ext.velox.views.sqla.delete import MultiDeleteObjectView
    from yourapp import db
    from yourapp.models import MyModel

    class MyView(MultiDeleteObjectView):
        model = MyModel
        session = db.session
        template = 'multi.html'

This view operates almost identically to the :ref:`delete-view` with a couple
of exceptions.

1. This view operates on POST rather GET
2. ``objects`` is returned to the context rather than ``object``.

Example Template
----------------

.. code-block:: html+jinja

    <form action="{{ url_for(request.url_rule.endpoint, confirm=True) }}" method="POST">
        <p>Are you sure?</p>
        <ul>
            {% for object in objects %}
            <li>{{ object }}</li>
            <input type="hidden" name="objects" id="objects" value="{{ object.id }}" />
            {% endfor %}
        </ul>
        <button type="submit">Do it!</button>
    </form>
