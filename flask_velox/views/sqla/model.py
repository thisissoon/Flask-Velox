# -*- coding: utf-8 -*-

"""
Module provides classes for rendering views for SQLAlchemy based models.

Note
----
Flask SQLAlchemy must be installed
"""

from flask_velox.mixins.context import ContextMixin
from flask_velox.mixins.sqla.model import ListModelMixin, TableModelMixin
from flask_velox.mixins.template import TemplateMixin


class ModelListView(ListModelMixin, ContextMixin, TemplateMixin):
    """ Handles rendering templates which list out model objects.

    Example
    -------
    >>> from flask import Flask
    >>> from flask.ext.sqlalchemy import SQLAlchemy
    >>> from flask.ext.velox.views.sqla.model import ModelListView
    >>> from yourapp.models import SomeModel
    ...
    >>> app = Flask(__name__)
    >>> db = SQLAlchemy(app)
    ...
    >>> class MyListView(ModelListView):
    ...     template = 'templates/list.html'
    ...     session = db.session
    ...     model = SomeModel
    ...
    >>> app.add_url_rule('/', view_func=MyListView.as_view('list'))
    ...
    >>> app.run()

    """

    def get(self):
        """ Handle HTTP GET requests using Flask ``MethodView`` rendering a
        single html template.

        Note
        ----
        This overrides :py:meth:`flask_velox.mixins.template.TemplateMixin.get`
        adding the following to the context:

        * ``objects``: List of objects to iterate
        * ``paginatation``: Pagination object for paging objects or None

        Returns
        -------
        str
            Rendered template
        """

        objects, pagination = self.get_objects()

        self.add_context('objects', objects)
        self.add_context('pagination', pagination)

        return super(ModelListView, self).get()


class TableModelView(TableModelMixin, ModelListView):
    """ View renders model lists in a table extending :py:class:`ModelListView`
    adding extra attributes to configure the table output.
    """

    def get(self):
        """ Handle HTTP GET requests using Flask ``MethodView`` rendering a
        single html template.

        Note
        ----
        This overrides :py:meth:`ModelListView.get` adding the following
        context attributes:

        * ``columns``: List of columns
        * ``column_name``: Function used to get human freindly names
        * ``format_value``: Function used to format output field values

        Returns
        -------
        str
            Rendered template
        """

        self.add_context('columns', self.get_columns())
        self.add_context('column_name', self.column_name)
        self.add_context('format_value', self.format_value)

        return super(TableModelView, self).get()
