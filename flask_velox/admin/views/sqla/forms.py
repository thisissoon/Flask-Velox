# -*- coding: utf-8 -*-

"""
Module provides classes for rendering views / forms for SQLAlchemy based models
within ``Flask-Admin`` systems.

Note
----
The following packages must be installed.

* Flask-SQLAlchemy
* Flask-WTForms
* Flask-Admin
"""

from flask_velox.admin.mixins.template import AdminTemplateMixin
from flask_velox.admin.mixins.sqla.forms import AdminModelFormMixin
from flask_velox.mixins.sqla.forms import (
    CrateModelFormMixin,
    UpdateModelFormMixin)
from flask_velox.views.sqla.forms import BaseModelView


class AdminBaseModelView(
        AdminModelFormMixin,
        AdminTemplateMixin,
        BaseModelView):
    """ Base View for Admin Create and Update views.
    """

    def post(self, admin, *args, **kwargs):
        """ Hadnle HTTP POST requests. Overrides default ``post`` behaviour
        allowing the view on POST reqeuests to be processed by ``Flask-Admin``

        See Also
        --------
        * :py:meth:`flask_velox.views.forms.BaseModelView.post`

        Returns
        -------
        str
            Rendered template
        """

        self._admin = admin
        return super(AdminBaseModelView, self).render()


class AdminCreateModelView(CrateModelFormMixin, AdminBaseModelView):
    """ Implements ``CrateModelFormMixin`` for ``Flask-Admin``.

    See Also
    --------
    * :py:class:`flask_velox.mixins.sqla.forms.CrateModelFormMixin`

    Attributes
    ----------
    template : str
        Relative template path, defaults to ``admin/forms/create.html``
    """

    template = 'admin/forms/create.html'


class AdminUpdateModelView(UpdateModelFormMixin, AdminBaseModelView):
    """ Implements ``UpdateModelFormMixin`` for ``Flask-Admin``.

    See Also
    --------
    * :py:class:`flask_velox.mixins.sqla.forms.UpdateModelFormMixin`

    Attributes
    ----------
    template : str
        Relative template path, defaults to ``admin/forms/update.html``
    """

    template = 'admin/forms/update.html'

    def set_context(self):
        """ Set extra context variables specific to ``Flask-Admin`` update
        views.

        See Also
        --------
        * :py:meth:`from flask_velox.mixins.context.ContextMixin.set_context`
        """

        super(AdminUpdateModelView, self).set_context()

        self.merge_context({
            'object': self.get_object(),
            'delete_url_rule': self.get_delete_url_rule(),
            'delete_url': self.delete_url
        })
