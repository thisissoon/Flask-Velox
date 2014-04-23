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

    pass


class TableModelView(TableModelMixin, ModelListView):
    """ View renders model lists in a table extending :py:class:`ModelListView`
    adding extra attributes to configure the table output.
    """

    pass
