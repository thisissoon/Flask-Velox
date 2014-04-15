# -*- coding: utf-8 -*-

"""
Module provides classes for rendering views for SQLAlchemy based models within
``Flask-Admin`` systems.

Note
----
Flask-SQLAlchemy must be installed
Flask-Admin must be installed
"""

from flask_velox.admin.mixins import AdminTemplateMixin
from flask_velox.views.sqla.model import ModelListView, TableModelView


class AdminModelListView(AdminTemplateMixin, ModelListView):

    template = 'admin/forms/list.html'


class AdminModelTableView(AdminTemplateMixin, TableModelView):

    template = 'admin/forms/table.html'
