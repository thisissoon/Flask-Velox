# -*- coding: utf-8 -*-

""" Mixin classes for forms specific to ``Flask-Admin`` and ``Flask-WTForms``

Note
----
The following packages must be installed.

* ``Flask-WTF``
* ``Flask-Admin``
"""

from flask import url_for
from flask_velox.admin.mixins.template import AdminTemplateMixin
from flask_velox.mixins.context import ContextMixin
from flask_velox.mixins.forms import FormMixin, MultiFormMixin


class AdminBaseFormMixin(ContextMixin, AdminTemplateMixin):
    """ Base Admin Form Mixin.

    Warning
    -------
    Use this mixin inconjunction with other mixins, cannot be used on its
    own.

    Attributes
    ----------
    cancel_url_rule : str, optional
        Flask url rule for cancel link, defaults to ``.index``
    """

    def set_context(self):
        """ Adds extra context variables.

        Note
        ----
        Adds the following extra context variables:

        * ``cancel_url_rule``: str
        * ``cancel_url``: func

        See Also
        --------
        * :py:meth:`from flask_velox.mixins.context.ContextMixin.set_context`

        """

        super(AdminBaseFormMixin, self).set_context()

        self.merge_context({
            'cancel_url_rule': self.get_cancel_url_rule(),
            'cancel_url': self.cancel_url
        })

    def get_redirect_url_rule(self):
        """ Returns raw redirect url rule to be used in ``url_for``. If the
        ``redirect_url_rule`` is not defined then ``.index``  will be
        returned.

        Returns
        -------
        str
            Raw flask url endpoint
        """

        return getattr(self, 'redirect_url_rule', '.index')

    def get_cancel_url_rule(self):
        """ Returns the ``cancel_url_rule`` or raises NotImplementedError if
        not defined.

        Returns
        -------
        str
            Defined ``cancel_url_rule``
        """

        return getattr(self, 'cancel_url_rule', '.index')

    def cancel_url(self, **kwargs):
        """ Returns the url to a cancel endpoint, this is used to render a link
        in forms to exit::

            <a href="{{ cancel_url() }}">Cancel</a>

        The ``cancel_url_rule`` must be defined.

        See Also
        --------
        * :py:meth:`get_cancel_url_rule`

        Arguments
        ---------
        \*\*kwargs
            Arbitrary keyword arguments passed to ``Flask.url_for``

        Returns
        -------
        str or None
            Generated url
        """

        rule = self.get_cancel_url_rule()
        return url_for(rule, **kwargs)

    def get_delete_url_rule(self):
        """ Returns the ``delete_url_rule`` or None if not defined.

        Returns
        -------
        str or None
            Defined ``delete_url_rule``
        """

        return getattr(self, 'delete_url_rule', '.delete')

    def delete_url(self, **kwargs):
        """ Returns the url to a delete endpoint, this is used to render a link
        in forms to delete an object::

            <a href="{{ delete_url(id=object.id) }}">Cancel</a>

        If ``delete_url_rule`` is not defined this method will not be called.

        See Also
        --------
        * :py:meth:`get_delete_url_rule`

        Arguments
        ---------
        \*\*kwargs
            Arbitrary keyword arguments passed to ``Flask.url_for``

        Returns
        -------
        str or None
            Generated url
        """

        rule = self.get_delete_url_rule()
        return url_for(rule, **kwargs)

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
        return super(AdminBaseFormMixin, self).render()


class AdminFormMixin(AdminBaseFormMixin, FormMixin):
    """ Admin form mixin class provides the ability to render forms within
    the ``Flask-Admin`` System for an SQLAlchemy model.
    """

    pass


class AdminMultiFormMixin(AdminBaseFormMixin, MultiFormMixin):
    """ Admin form mixin class provides the ability to render multiple forms
    within the ``Flask-Admin`` System for an SQLAlchemy model.
    """

    pass
