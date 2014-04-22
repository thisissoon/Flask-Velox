# -*- coding: utf-8 -*-

"""
Module provides classes for rendering views / forms for SQLAlchemy based models
within ``Flask-Admin`` systems.

Note
----
The following packages must be installed:

* Flask-SQLAlchemy
* Flask-WTForms
* Flask-Admin
"""

from flask_velox.admin.mixins.forms import AdminFormMixin, AdminMultiFormMixin
from flask_velox.mixins.sqla.forms import (
    CreateModelFormMixin,
    UpdateModelFormMixin,
    UpdateModelMultiFormMixin)


class AdminCreateModelView(CreateModelFormMixin, AdminFormMixin):
    """ Implements ``CreateModelFormMixin`` for ``Flask-Admin``.

    See Also
    --------
    * :py:class:`flask_velox.mixins.sqla.forms.CreateModelFormMixin`

    Attributes
    ----------
    template : str
        Relative template path, defaults to ``admin/forms/create.html``
    """

    template = 'velox/admin/create.html'


class AdminUpdateModelView(UpdateModelFormMixin, AdminFormMixin):
    """ Implements ``UpdateModelFormMixin`` for ``Flask-Admin``.

    See Also
    --------
    * :py:class:`flask_velox.mixins.sqla.forms.UpdateModelFormMixin`

    Attributes
    ----------
    template : str
        Relative template path, defaults to ``admin/forms/update.html``
    """

    template = 'velox/admin/update.html'

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


class AdminUpdateMultiFormView(UpdateModelMultiFormMixin, AdminMultiFormMixin):
    """ Implements ``UpdateModelFormMixin`` for ``Flask-Admin`` with
    multiple forms.

    See Also
    --------
    * :py:class:`flask_velox.mixins.sqla.forms.UpdateModelFormMixin`

    Attributes
    ----------
    template : str
        Relative template path, defaults to ``admin/forms/update.html``
    """

    template = 'velox/admin/update_multi_form.html'

    def set_context(self):
        """ Set extra context variables specific to ``Flask-Admin`` update
        views.

        See Also
        --------
        * :py:meth:`from flask_velox.mixins.context.ContextMixin.set_context`
        """

        super(AdminUpdateMultiFormView, self).set_context()

        self.merge_context({
            'object': self.get_object(),
            'delete_url_rule': self.get_delete_url_rule(),
            'delete_url': self.delete_url
        })
