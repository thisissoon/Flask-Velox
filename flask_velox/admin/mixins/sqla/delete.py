# -*- coding: utf-8 -*-

""" Provides mixin classes to delete SQLAlchemy objects from within
a ``Flask-Admin`` interface.

Note
----
The following packages must be installed:

* Flask-SQLAlchemy
* Flask-Admin
"""

from flask import url_for
from flask_velox.admin.mixins.template import AdminTemplateMixin
from flask_velox.mixins.sqla.delete import (
    DeleteObjectMixin,
    MultiDeleteObjectMixin)


class AdminDeleteBaseMixin(object):
    """ Base mixin class to be used inconjunction with other mixin classes.
    """

    def set_context(self):
        """ Adds extra context variables to be used in delete view templates.

        See Also
        --------
        * :py:meth:`from flask_velox.mixins.context.ContextMixin.set_context`

        Note
        ----
        Adds the following context variables:

        * ``object``: The object to be deleted
        * ``cancel_url``: Function for retrieving cancel url in template
        """

        super(AdminDeleteBaseMixin, self).set_context()

        self.add_context('cancel_url', self.cancel_url)

    def get_cancel_url_rule(self):
        """ Returns the ``cancel_url_rule`` or if not defined returns default
        value of ``.index``.

        Returns
        -------
        str
            Defined ``cancel_url_rule``
        """

        return getattr(self, 'cancel_url_rule', '.index')

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

    def redirect_url(self, **kwargs):
        """ Returns the url to a redirect endpoint, when the form is valid
        and the callback is called.

        See Also
        --------
        * :py:meth:`get_redirect_url_rule`

        Arguments
        ---------
        \*\*kwargs
            Arbitrary keyword arguments passed to ``Flask.url_for``

        Returns
        -------
        str or None
            Generated url
        """

        rule = self.get_redirect_url_rule()
        return url_for(rule, **kwargs)


class AdminDeleteObjectMixin(
        AdminDeleteBaseMixin,
        DeleteObjectMixin,
        AdminTemplateMixin):
    """ Mixin provides object deletion support from within a ``Flask-Admin``
    system.

    See Also
    --------
    * :py:class:`flask_velox.mixins.sqla.delete.DeleteObjectMixin`

    Attributes
    ----------
    redirect_url_rule : str, optional
        Raw flask url to send users on success, defaults to ``.index``
    cancel_url_rule : str, optional
        Raw flask url to send users on cancel, defaults to ``.index``
    """

    pass


class AdminMultiDeleteObjectMixin(
        AdminDeleteBaseMixin,
        MultiDeleteObjectMixin,
        AdminTemplateMixin):
    """ Mixin provides multi object deletion support from within a
    ``Flask-Admin`` system.

    See Also
    --------
    * :py:class:`flask_velox.mixins.sqla.delete.MultiDeleteObjectMixin`

    Attributes
    ----------
    redirect_url_rule : str, optional
        Raw flask url to send users on success, defaults to ``.index``
    cancel_url_rule : str, optional
        Raw flask url to send users on cancel, defaults to ``.index``
    """

    def post(self, admin, *args, **kwargs):
        """ Overrides post method in order to capture admin view for
        rendering within admin system.
        """

        self._admin = admin
        return super(AdminMultiDeleteObjectMixin, self).post(*args, **kwargs)
