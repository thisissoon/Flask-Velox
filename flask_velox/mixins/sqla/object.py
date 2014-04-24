# -*- coding: utf-8 -*-

""" Mixin classes for obtaining object of an SQLAlchemy model.

Note
----
The following packages must be installed:

* Flask-SQLAlchemy
"""

from flask import request
from flask_velox.mixins.sqla.read import BaseModelMixin


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
