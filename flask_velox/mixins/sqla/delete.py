# -*- coding: utf-8 -*-

""" Mixin classes for deleting SQLAlchemy objects from the Database.

Note
----
The following packages must be installed:

* Flask-SQLAlchemy
"""

from flask import flash, request
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
    confirm : bool, optional
        Ensure a confirmed flag is required when processing the view,
        defaults to ``True``
    """

    def __init__(self, *args, **kwargs):
        """ Constructor. Invokes the object deletion process.
        """

        super(DeleteObjectMixin, self).__init__(*args, **kwargs)

        self.delete()

    @property
    def can_delete(self):
        """ Propery function which returns a bool. If ``confirm`` attribute
        is set to ``False`` on the class this will return ``True`` else it
        will only return ``True`` if the ``confirmed`` query string is
        present.

        Returns
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

    def flash(self):
        """ Flashes a success message to the user.
        """

        obj = self.get_object()  # will be cached in self._obj
        flash('{0} was successfuly deleted'.format(obj), 'success')

    def success_callback(self):
        """ Success callback called after object has been deleted.
        Override this to customise what happens after an object is delted

        Raises
        ------
        werkzeug.routing.RequestRedirect
            When object is deleted to force a redirect to another View
        """

        self.flash()

        raise RequestRedirect(self.redirect_url())

    def delete(self):
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


class MultiDeleteObjectMixin(DeleteObjectMixin):
    """ Mixin provides functionality to delete mutliple objects of the same
    model.
    """

    #: Allowed HTTP Methods
    methods = ['GET', 'POST', ]

    def set_context(self):
        """ Override context to add objects rather than object to the
        context.
        """

        super(MultiDeleteObjectMixin, self).set_context()

        self.add_context('objects', self.get_objects())

    def get_objects(self):
        """ Returns a set of objects set for deletion. List of objects is
        retrived from a HTTP POST list called ``objects``.

        Returns
        -------
        set
            Set of objects to delete
        """

        try:
            return self._objs
        except AttributeError:

            objects = set()
            model = self.get_model()

            # Values to use in object lookup, could id for example or slug etc
            vals = request.values.getlist('objects')

            try:
                field = getattr(model, self.get_lookup_field())
            except AttributeError:
                raise AttributeError('Lookup field does not exist')

            for obj in model.query.filter(field.in_(vals)).all():
                objects.add(obj)

            self._objs = objects
            return objects

    def flash(self):
        """ Flashes a success message to the user.
        """

        objs = self.get_objects()
        flash('{0} objects successfuly deleted'.format(len(objs)), 'success')

    def delete(self):
        """ Override default delete functionality adding the ability to
        delete multiple objects of the same model but only if
        :py:meth:`can_delete` is ``True``.
        """

        # Only delete if ?confirmed=True or confirm = False
        if self.can_delete:

            session = self.get_session()
            for obj in self.get_objects():
                session.delete(obj)

            session.commit()  # Delete happens here

            # Call the callback
            self.success_callback()

    def post(self, *args, **kwargs):
        """ Handle HTTP POST requests rendering a template.
        """

        return self.render()
