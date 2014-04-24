# -*- coding: utf-8 -*-

""" Provides views for delete SQLAlchemy objects from within a ``Flask-Admin``
interface.

Note
----
The following packages must be installed:

* Flask-SQLAlchemy
* Flask-Admin
"""

from flask_velox.admin.mixins.sqla.delete import (
    AdminDeleteObjectMixin,
    AdminMultiDeleteObjectMixin)


class AdminDeleteObjectView(AdminDeleteObjectMixin):
    """ Admin View for deleting a single SQL Alchemy object. Defines
    default template.
    """

    template = 'velox/admin/delete.html'


class AdminMultiDeleteObjectView(AdminMultiDeleteObjectMixin):
    """ Admin view for SQLAlchemy multi object deletion. Defines default
    template and implements HTTP POST request handling.
    """

    template = 'velox/admin/delete_multiple.html'
