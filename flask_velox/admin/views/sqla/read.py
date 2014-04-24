# -*- coding: utf-8 -*-

"""
Module provides classes for rendering views for SQLAlchemy based models within
``Flask-Admin`` systems.

Note
----
The following packages must be installed.

* ``Flask-SQLAlchemy``
* ``Flask-Admin``
"""

from flask_velox.admin.mixins.sqla.read import AdminTableModelMixin
from flask_velox.admin.mixins.template import AdminTemplateMixin
from flask_velox.views.sqla.read import ModelListView, TableModelView


class AdminModelListView(AdminTemplateMixin, ModelListView):

    template = 'admin/forms/list.html'


class AdminModelTableView(
        AdminTemplateMixin,
        AdminTableModelMixin,
        TableModelView):
    """ Extends the :py:class:`flask_velox.views.sqla.model.TableModelView`
    view injecting an admin specific mixin extending the functionality
    of the view.

    See Also
    --------
    * :py:class:`flask_velox.admin.mixins.sqla.model.AdminTableModelMixin`
    """

    template = 'velox/admin/table.html'
