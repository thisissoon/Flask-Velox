# -*- coding: utf-8 -*-

""" Mixin classes for deleting SQLAlchemy objects from the Database.

Note
----
The following packages must be installed:

* Flask-SQLAlchemy
"""

from flask import flash, request, url_for
from flask_velox.mixins.template import TemplateMixin
from flask_velox.mixins.context import ContextMixin
from flask_velox.mixins.sqla.object import SingleObjectMixin
from werkzeug.routing import RequestRedirect


class DeleteObjectMixin(SingleObjectMixin, ContextMixin, TemplateMixin):
    """ Deletes a single SQLAlchemy object from the Database.

    Example
    -------

    .. code-block:: python
        :linenos:

        form flask.ext.velox.mixins.sqla.delete import DeleteObjectMixin
        from yourapp import db
        from yourapp.models import MyModel

        class DeleteMyModel(DeleteObjectMixin):
            template = 'delete.html'
            model = MyModel
            session = db.sesion

    Attributes
    ----------
    confirm : bool
        Ensure a confirmed flag is required when processing the view,
        defaults to ``True``
    """

    def __init__(self, *args, **kwargs):
        """ Constructor. Invokes the object deletion process.
        """

        super(DeleteObjectMixin, self).__init__(*args, **kwargs)

        self.delete_object()

    @property
    def can_delete(self):
        """ Propery function which returns a bool. If ``confirm`` attribute
        is set to ``False`` on the class this will return ``True`` else it
        will only return ``True`` if the ``confirmed`` query string is
        present.

        Retruns
        -------
        bool
            Ok to delete the object or not
        """

        if getattr(self, 'confirm', True):
            return bool(request.args.get('confirm', False))

        return True

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

        super(DeleteObjectMixin, self).set_context()

        self.add_context('object', self.get_object())
        self.add_context('cancel_url', self.cancel_url)

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

    def success_callback(self):
        """ Success callback called after object has been deleted.
        Override this to customise what happens after an object is delted

        Raises
        ------
        werkzeug.routing.RequestRedirect
            When object is deleted to force a redirect to another View
        """

        obj = self.get_object()  # will be cached in self._obj

        flash('{0} was successfuly deleted'.format(obj), 'success')

        try:
            rule = self.redirect_url_rule
        except AttributeError:
            raise NotImplementedError('``redirect_url_rule`` required.')

        raise RequestRedirect(url_for(rule))

    def delete_object(self):
        """ Deletes the object, only if :py:meth:`can_delete` returns ``True``.
        """

        # Only delete if ?confirmed=True or confirm = False
        if self.can_delete:

            # Get the sesion and object
            session = self.get_session()
            obj = self.get_object()

            # Delete the object
            session.delete(obj)
            session.commit()  # Delete happens here

            # Call the callback
            self.success_callback()
