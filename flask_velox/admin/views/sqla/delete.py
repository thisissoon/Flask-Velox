# -*- coding: utf-8 -*-

""" Provides views for delete SQLAlchemy objects from within a ``Flask-Admin``
interface.

Note
----
The following packages must be installed:

* Flask-SQLAlchemy
* Flask-Admin
"""

from flask_velox.admin.mixins.template import AdminTemplateMixin
from flask_velox.views.sqla.delete import (
    DeleteObjectView,
    MultiDeleteObjectView)


class AdminDeleteObjectView(DeleteObjectView, AdminTemplateMixin):
    """ Admin View for deleting a single SQL Alchemy object. Defines
    default template.

    Attributes
    ----------
    template : str
        Template to render, defaults to ``admin/forms/delete.html``
    """

    template = 'velox/admin/delete.html'


class AdminMultiDeleteObjectView(MultiDeleteObjectView, AdminTemplateMixin):
    """ Admin view for SQLAlchemy multi object deletion. Defines default
    template and implements HTTP POST request handling.

    Attributes
    ----------
    template : str
        Template to render, defaults to ``admin/forms/delete.html``
    """

    template = 'velox/admin/delete_multiple.html'

    def post(self, admin, *args, **kwargs):

        self._admin = admin
        return super(AdminMultiDeleteObjectView, self).post(*args, **kwargs)
