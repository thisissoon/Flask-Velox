# -*- coding: utf-8 -*-

"""
Module provides classes for rendering views for SQLAlchemy based models.

Note
----
The following packages must be installed:

* ``Flask SQLAlchemy``
"""

from flask_velox.mixins.context import ContextMixin
from flask_velox.mixins.sqla.read import ListModelMixin, TableModelMixin
from flask_velox.mixins.template import TemplateMixin


class ModelListView(ListModelMixin, ContextMixin, TemplateMixin):
    """ Handles rendering templates which list out model objects.

    Example
    -------

    .. code-block:: python
        :linenos:

        from flask import Flask
        from flask.ext.sqlalchemy import SQLAlchemy
        from flask.ext.velox.views.sqla.model import ModelListView
        from yourapp.models import SomeModel

        app = Flask(__name__)
        db = SQLAlchemy(app)

        class MyListView(ModelListView):
            template = 'templates/list.html'
            session = db.session
            model = SomeModel

        app.add_url_rule('/', view_func=MyListView.as_view('list'))

        app.run()

    """

    def set_context(self):
        """ Adds extra context to SQLAlchemy based list views.

        See Also
        --------
        * :py:meth:`from flask_velox.mixins.context.ContextMixin.set_context`

        Note
        ----
        Adds the following context variables.

        * ``objects``: List of model objects
        * ``pagination``: Pagination object or ``None``

        Returns
        -------
        str
            Rendered template
        """

        super(ModelListView, self).set_context()

        objects, pagination = self.get_objects()

        self.add_context('objects', objects)
        self.add_context('pagination', pagination)


class TableModelView(TableModelMixin, ModelListView):
    """ View renders model lists in a table extending :py:class:`ModelListView`
    adding extra attributes to configure the table output.
    """

    def set_context(self):
        """ Adds extra context to SQLAlchemy table based list views.

        See Also
        --------
        * :py:meth:`from flask_velox.mixins.context.ContextMixin.set_context`

        Note
        ----
        Adds the following context variables.

        * ``columns``: List of columns
        * ``column_name``: ``column_name`` function
        * ``format_value``: ``format_value`` function

        Returns
        -------
        str
            Rendered template
        """

        super(TableModelView, self).set_context()

        self.add_context('columns', self.get_columns())
        self.add_context('column_name', self.column_name)
        self.add_context('format_value', self.format_value)
