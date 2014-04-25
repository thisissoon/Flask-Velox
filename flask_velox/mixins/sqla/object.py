# -*- coding: utf-8 -*-

""" Mixin classes for obtaining object of an SQLAlchemy model.

Note
----
The following packages must be installed:

* Flask-SQLAlchemy
"""

from flask import request
from flask_velox.mixins.context import ContextMixin


class BaseModelMixin(ContextMixin):
    """ Mixin provides SQLAlchemy model integration.

    Attributes
    ----------
    model : class
        SQLAlchemy un-instanciated model class
    session : object
        SQLAlchemy session instance
    pk_field : str, optional
        The primary key field name, defaults to ``id``
    """

    def set_context(self):
        """ Overrides ``set_context`` to set extra context variables.

        See Also
        --------
        * :py:meth:`from flask_velox.mixins.context.ContextMixin.set_context`
        """

        super(BaseModelMixin, self).set_context()

        self.add_context('model', self.get_model())

    def get_session(self):
        """ Returns the SQLAlchemy db session instance.

        Example
        -------
        >>> from flask.ext.velox.mixins.sqla.model import BaseModelMixin
        >>> from yourapp import db
        >>> class MyView(BaseModelMixin):
        ...     session = db.session
        >>> view = MyView()
        >>> view.get_session()
        <sqlalchemy.orm.scoping.scoped_session at 0x104c88dd0>

        Raises
        ------
        NotImplementedError
            If ``session`` has not been declared on the class

        """

        if not hasattr(self, 'session'):
            raise NotImplementedError('``session`` attribute required')

        return self.session

    def get_model(self):
        """ Returns the Model to perform queries against.

        Example
        -------
        >>> from flask.ext.velox.mixins.sqla.model import BaseModelMixin
        >>> from yourapp.models import SomeModel
        >>> class MyView(BaseModelMixin):
        ...     model = SomeModel
        >>> view = MyView()
        >>> view.get_model()
        yourapp.models.SomeModel

        Raises
        ------
        NotImplementedError
            If ``model`` has not been declared on the class

        """

        if not hasattr(self, 'model'):
            raise NotImplementedError('``model`` attribute required')

        return self.model

    def get_pk_field(self):
        """ Returns the primary key field name. If ``pk_field`` is not
        declared return value defaults to ``id``.

        Example
        -------
        >>> from flask.ext.velox.mixins.sqla.model import BaseModelMixin
        >>> class MyView(BaseModelMixin):
        ...     pk_field = 'foo'
        >>> view = MyView()
        >>> view.get_pk_field()
        'foo'

        Returns
        -------
        str
            Primary key field name

        """

        return getattr(self, 'pk_field', 'id')


class SingleObjectMixin(BaseModelMixin):
    """ Mixin handles retrieving a single object from an SQLAlchemy model.
    This is done by defining a field query.

    The value to use in the query is obtained by trying different ``request``
    attributes for the data:

    1. ``request.view_args`` - Data passed as part of a uri
    2. ``request.args`` - Data passed as part of aquery string
    3. ``self`` - An attribute defined on the view class

    The field used for the lookup is also the name of the value passed in the
    request, for example if ``lookup_field`` is set to ``foo`` then
    ``request.view_args`` / ``request.args`` should have an element
    named ``foo`` containing the data **or** an attribute on the class
    named ``foo``.

    Examples
    --------

    .. code-block:: python
        :linenos:

        from flask.ext.velox.mixins.sqla.object import SingleObjectMixin
        from yourapp.models import MyModel

        class MyView(SingleObjectMixin):
            model = MyModel
    """

    def get_lookup_field(self):
        """ Returns the field to lookup objects against, if ``lookup_field``
        is not defined ``id`` will be returned by default.

        Returns
        -------
        str
            Field to use for lookup, defaults to ``id``
        """

        return getattr(self, 'lookup_field', 'id')

    def get_lookup_value(self):
        """ Attempt to get the value to use for looking up the object in
        the database, this is usually an id number but could technically
        be anything.

        Returns
        -------
        anything
            Value to use in the lookup query
        """

        field = self.get_lookup_field()

        # First check if view args contains the data
        val = request.view_args.get(field)

        if not val:

            # Second check if request.args has the data
            val = request.args.get(field)

        if not val:

            # Third check if the instance has a attribute with the data
            val = getattr(self, field, None)

        return val

    def get_object(self):
        """ Returns an object from the database or a blank object if no
        lookup value is provided.

        Returns
        -------
        object
            Populated or blank model object
        """

        if hasattr(self, '_obj'):
            return self._obj

        model = self.get_model()
        val = self.get_lookup_value()

        if val:
            filter_by = {
                self.get_lookup_field(): val}
            obj = model.query.filter_by(**filter_by).first()
        else:
            obj = model()

        self._obj = obj

        return obj
