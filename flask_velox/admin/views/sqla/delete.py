# -*- coding: utf-8 -*-

""" Provides views for delete SQLAlchemy objects from within a ``Flask-Admin``
interface.

Note
----
The following packages must be installed.

* Flask-SQLAlchemy
* Flask-Admin
"""

from flask_velox.admin.mixins.template import AdminTemplateMixin
from flask_velox.views.sqla.delete import DeleteObjectView


class AdminDeleteObjectView(AdminTemplateMixin, DeleteObjectView):
    """
    """

    template = 'admin/forms/delete.html'
