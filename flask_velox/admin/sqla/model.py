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
from flask_velox.views.sqla.model import ModelListView


class AdminModelListView(AdminTemplateMixin, ModelListView):
    """ Overrides defult ``ModelListView`` providing the ability to render
    list views in ``Flask-Admin`` systems.
    """

    template = 'admin/forms/list.html'

    def get(self, admin):
        """ Handles HTTP GET requests to View. Also sets ``self._admin``
        which contains the passed admin view.

        Arguments
        ---------
        admin : obj
            The current admin view

        Note
        ----
        Overrides: :py:meth:`flask_velox.admin.mixins.AdminTemplateMixin.get`
        """

        return super(AdminModelListView, self).get(admin)
