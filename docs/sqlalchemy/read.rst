Read
====

Reading SQLAlchemy models in views is simple.

Model List View
---------------

.. seealso::

    * :py:class:`flask_velox.mixins.sqla.read.ListModelMixin`

The ``ModelListView`` allows you to render templates with paginated (or not)
lists of model objects.

.. code-block:: python

    from flask.ext.velox.views.sqla import read
    from yourapp.models import Model

    class MyView(read.ModelListView):
        model = Model
        template = 'list.html'

The context returned to the template is as follows:

* ``model``: The SQLAlchemy model class
* ``objects``: List of objects returned from query
* ``pagination``: Pagination object or ``None``

Pagination
~~~~~~~~~~

``Flask-SQLAlchemy`` gives us pagination if we want it, by default ``paginate``
is ``True`` and the number of records is limited to 30, but this can all be
changed and configured.

No Pagination
^^^^^^^^^^^^^

.. code-block:: python

    class MyView(read.ModelListView):
        model = Model
        template = 'list.html'
        paginate = False

Set records per page
^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    class MyView(read.ModelListView):
        model = Model
        template = 'list.html'
        per_page = 10

Example Template
~~~~~~~~~~~~~~~~

Here are some example templates.

Without Pagination
^^^^^^^^^^^^^^^^^^

.. code-block:: html+jinja

    <ul>
        {% for object in objects %}
        <li>{{ object.name }}</li>
        {% endfor %}
    </ul>

With Pagination
^^^^^^^^^^^^^^^

.. code-block:: html+jinja

    <ul>
        {% for object in objects %}
        <li>{{ object.name }}</li>
        {% endfor %}
    </ul>

    {% if objects.has_prev %}<a href="{{ url_for('rule', page=objects.prev_num) }}"><< Newer Objects{% else %}<< Newer Objects{% endif %} |
    {% if objects.has_next %}<a href="{{ url_for('rule', page=objects.next_num) }}">Older Objects >></a>{% else %}Older Objects >>{% endif %}

Changing context name
~~~~~~~~~~~~~~~~~~~~~

If you do not wish ``objects`` to be used as the context name for your object
list you can change this be defining a ``objects_context_name`` attribute on
the class, for example:

.. code-block:: python

    from flask.ext.velox.views.sqla import read
    from yourapp.models import Model

    class MyView(read.ModelListView):
        model = Model
        objects_context_name = 'foos'
        template = 'list.html'

In this case ``foos`` will be used instead of ``objects`` in the template.

Model Table View
----------------

The table model view is almost exactly the same as ``ModelListView`` so we
won't tread the same ground.

This view allows us to specify the columns we want to render in our table which
relate to field names in the model:

.. code-block:: python

    from flask.ext.velox.views.sqla import read
    from yourapp.models import Model

    class MyView(read.ModelTableView):
        model = Model
        template = 'list.html'
        columns = ['field1', 'field2', 'field3']
        paginate = False

The context returned to the template is as follows:

* ``model``: The SQLAlchemy model class
* ``objects``: List of objects returned from query
* ``pagination``: Pagination object or ``None``
* ``columns``: List of columns to render
* ``column_name``: Function to make the column name humanized
* ``format_value``: Function to format a fields value

Template Example
~~~~~~~~~~~~~~~~

.. code-block:: html+jinja
    :linenos:
    :emphasize-lines: 5, 13

    <table>
        <thead>
            <tr>
                {% for column in columns %}
                <th>{{ column_name(column) }}</th>
                {% endfor %}
            </tr>
        </thead>
        <tbody>
            {% for object in objects %}
            <tr>
                {% for column in columns %}
                <tr>{{ format_value(column, object) }}
                {% endfor %}
            </tr>
            {% endfor %}
        </tbody>
    </table>

We won't go into detail about how ``column_name`` and ``format_value`` work
here but you can check the :doc:`/api` for more details:

* :py:meth:`flask_velox.mixins.sqla.read.TableModelMixin.column_name`
* :py:meth:`flask_velox.mixins.sqla.read.TableModelMixin.format_value`

Pagination operates exactly the same as ``ListModelMixin``.

Object View
-----------

The ``ObjectView`` functions like the list views above however simply returns a
single object to the template. Please read the ``SingleObjectMixin``
documentation which explains how an object is retreived.

.. seealso::

    * :py:class:`flask_velox.mixins.sqla.read.ObjectMixin`
    * :py:class:`flask_velox.mixins.sqla.object.SingleObjectMixin`

.. code-block:: python

    from flask.ext.velox.views.sqla import read
    from yourapp.models import Model

    class MyView(read.ObjectView):
        model = Model
        template = 'detail.html'

The context returned to the template is as follows:

* ``model``: The SQLAlchemy model class
* ``object``: The object

Example Template
~~~~~~~~~~~~~~~~

.. code-block:: html+jinja

    <html>
        <head>
            <meta charset="utf-8" />
            <title>{{ object.name }}</title>
        </head>
        <body>
            {{ object.description }}
        </body>
    </html>

Changing context name
~~~~~~~~~~~~~~~~~~~~~

As with the list views you can change the context name used for accessing the
object in the template by setting an ``object_context_name`` attribute on the
view class:

.. code-block:: python

    from flask.ext.velox.views.sqla import read
    from yourapp.models import Model

    class MyView(read.ObjectView):
        model = Model
        template = 'detail.html'
        object_context_name = 'foo'

In the above view ``foo`` will be returned to the template for accessing the
object rather than ``object``.
