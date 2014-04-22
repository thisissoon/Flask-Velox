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

    template = 'admin/forms/table.html'

    def set_context(self):
        """ Adds extra context to Admin Table Views for ``Flask-Admin``
        systems

        See Also
        --------
        * :py:meth:`from flask_velox.mixins.context.ContextMixin.set_context`

        Note
        ----
        Adds the following context variables.

        * ``create_url_rule``: The raw url rule or ``None``
        * ``create_url``: Create url method
        * ``update_url_rule``: The raw url rule or ``None``
        * ``update_url``: Update url method
        * ``delete_url_rule``: The raw url rule or ``None``
        * ``delete_url``: Delete url method
        * ``with_selcted``: With selcted values
        """

        super(AdminModelTableView, self).set_context()

        self.merge_context({
            'create_url_rule': self.get_create_url_rule(),
            'create_url': self.create_url,
            'update_url_rule': self.get_update_url_rule(),
            'update_url': self.update_url,
            'delete_url_rule': self.get_delete_url_rule(),
            'delete_url': self.delete_url,
            'with_selected': self.get_with_selected(),
        })
