# -*- coding: utf-8 -*-

""" Mixin classes specific to ``Flask-Admin`` and ``Flask-SQLAlchemy``
based views with ``Flask-WTForms``

Note
----
The following packages must be installed.

* ``Flask-SQLAlchemy``
* ``Flask-WTForms``
* ``Flask-Admin``
"""

from flask import url_for
from flask_velox.mixins.sqla.forms import ModelFormMixin


class AdminModelFormMixin(ModelFormMixin):
    """
    Attributes
    ----------
    cancel_url_rule : str
        Flask url rule for cancel link
    """

    def set_context(self):
        """ Adds extra context variables, specifically:

        * ``cancel_url_rule``: str
        * ``cancel_url``: func

        See Also
        --------
        * :py:meth:`from flask_velox.mixins.context.ContextMixin.set_context`
        """

        super(AdminModelFormMixin, self).set_context()

        self.merge_context({
            'cancel_url_rule': self.get_cancel_url_rule(),
            'cancel_url': self.cancel_url
        })

    def get_cancel_url_rule(self):
        """ Returns the ``cancel_url_rule`` or raises NotImplementedError if
        not defined.

        Returns
        -------
        str
            Defined ``cancel_url_rule``

        Raises
        ------
        NotImplementedError
            If ``cancel_url_rule`` is not defined
        """

        try:
            return self.cancel_url_rule
        except AttributeError:
            raise NotImplementedError('``cancel_url_rule`` must be defined')

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

        return getattr(self, 'delete_url_rule', None)

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
