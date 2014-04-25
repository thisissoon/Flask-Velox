# -*- coding: utf-8 -*-

"""
Module provides mixin classes for dealing with SQLALchemy models

Note
----
The following packages must be installed:

* ``Flask SQLAlchemy``

Example
-------

.. code-block:: python
    :linenos:

    from flask.ext.velox.mixins.sqla.model import ModelMixin
    from yourapp import db
    from yourapp.models import SomeModel

    app = Flask(__name__)

    class MyView(ModelMixin):
        session = db.session
        model = SomeModel

"""

from flask import request
from flask_velox.mixins.sqla.object import BaseModelMixin, SingleObjectMixin


class ListModelMixin(BaseModelMixin):
    """ Mixin provides ability to list multiple instances of a SQLAlchemy
    model.

    As well as attributes supported by the classes this mixin inherits from
    other attributes are supported as well.

    Example
    -------

    .. code-block:: python
        :linenos:

        from flask.ext.velox.mixins.sqla.model import ListModelMixin
        from yourapp.models import SomeModel

        class MyView(ListModelMixin):
            model = SomeModel
            base_query = SomeModel.query.filter(foo='bar')

    Attributes
    ----------
    base_query : object, optional
        A SQLAlchemy base query object, if defined this will be used instead
        of ``self.model.query.all()``
    objects_context_name : str, optional
        Instead of using ``object`` you can set the context variable name to
        use for the object, defaults to ``object``
    paginate : bool, optional
        Paginate the records using SQLAlchemy ``query.paginate``, defaults True
    per_page : int, optional
        If ``paginate`` is ``True`` customise the number of records to show
        per page, defaults to ``30``
    """

    def set_context(self):
        """ Adds extra context to SQLAlchemy based list views.

        See Also
        --------
        * :py:meth:`from flask_velox.mixins.context.ContextMixin.set_context`

        Note
        ----
        Adds the following context variables.

        * ``objects``: List of model objects
        * ``pagination``: Pagination object or ``None``

        Returns
        -------
        str
            Rendered template
        """

        super(ListModelMixin, self).set_context()

        objects, pagination = self.get_objects()

        self.add_context(self.get_objects_context_name(), objects)
        self.add_context('pagination', pagination)

    def get_objects_context_name(self):
        """ Returns the context name to use when returning the objects to
        the template, defaults to ``objects``.

        Returns
        -------
        str
            Name to use for context variable
        """

        return getattr(self, 'objects_context_name', 'objects')

    def get_basequery(self):
        """ Returns SQLAlchemy base query object instance, if ``base_query`` is
        declared this will be used as the base query, else
        ``self.model.query.all()`` will be used which would get all model
        objects.

        Returns
        -------
        ``flask_sqlalchemy.BaseQuery``
            A flask BaseQuery object instance

        """

        model = self.get_model()
        base_query = getattr(self, 'base_query', model.query)

        return base_query

    def get_per_page(self):
        """ Returns the number of records to show per page for paginated
        result sets. Defaults to ``30``

        Returns
        -------
        int
            Number of records per page
        """

        return getattr(self, 'num_per_page', 30)

    def get_page(self):
        """ Attempt to get the current page number, assumes a HTTP GET
        query param called ``page`` is availible in ``flask.request.args``
        which holds the page number.
        """

        try:
            page = int(request.args.get('page', 1))
        except ValueError:
            raise ValueError('page GET param must be number')

        return page

    def get_objects(self):
        """ Returns a list of objects and pagination object if ``paginate``
        is ``True``, else None will be returned when ``paginate`` is not set
        or ``False``.

        Returns
        -------
        tuple
            List of model object instances, Pagination object or None
        """

        query = self.get_basequery()

        if getattr(self, 'paginate', True):
            page = self.get_page()
            pagination = query.paginate(page, per_page=self.get_per_page())

            return pagination.items, pagination

        return query.all(), None


class TableModelMixin(ListModelMixin):
    """ Mixin extends the default ``ListModelMixin`` behaviour adding
    attributes for rendering lists in tables.

    Example
    -------

    .. code-block:: python
        :linenos:

        from flask.ext.velox.mixins.sqla.model import TableModelMixin
        from yourapp.models import SomeModel

        class MyView(TableModelMixin):
            model = SomeModel
            columns = ['field1', 'field2', 'field3']

    Attributes
    ----------
    columns : list
        A list of columns to render, this should map to model fields
    formatters : dict
        A dict of key value pairs mapping a field name (key) to a method
        which formats the fields data, for example::

            formatters = {
                'field1': fmt_bool
                'field1': fmt_datetime
            }

    """

    def set_context(self):
        """ Adds extra context to SQLAlchemy table based list views.

        See Also
        --------
        * :py:meth:`from flask_velox.mixins.context.ContextMixin.set_context`

        Note
        ----
        Adds the following context variables.

        * ``columns``: List of columns
        * ``column_name``: ``column_name`` function
        * ``format_value``: ``format_value`` function

        """

        super(TableModelMixin, self).set_context()

        self.add_context('columns', self.get_columns())
        self.add_context('column_name', self.column_name)
        self.add_context('format_value', self.format_value)

    def get_columns(self):
        """ Returns the list of columns defined for the View using this Mixin.

        Returns
        -------
        list
            List of strings of model field names

        Raises
        ------
        NotImplementedError
            If ``columns`` is not defined
        """

        try:
            return self.columns
        except AttributeError:
            raise NotImplementedError('``columns`` is not defined')

    def column_name(self, name):
        """ Attempts to get a human friendly  name for the column. First it
        will look for an ``info`` attribute on the model field, if present
        will then return ``label`` value of the ``info`` ``dict``. If not
        present this method will replace underscore characters with spaces and
        simply title case the individual words.

        An example model with an ``info`` attribute, this is the same
        behaviour as ``WTForms-Alchemy``::

            class MyModel(db.Model):
                field = db.Column(db.Unicode, info={
                    'label' = 'My Field'
                })

        Arguments
        ---------
        name : str
            The column name mapping to a model field attribute

        Returns
        -------
        str
            Human friendly field name
        """

        model = self.get_model()
        field = getattr(model, name)  # This could AttributeError

        try:
            name = field.info['label']
        except (AttributeError, KeyError):
            name = name.replace('_', ' ').title()

        return name

    def get_formatters(self):
        """ Return formatters defined for the View using this Mixin.

        Returns
        -------
        dict or None
            Returns defined formatters or None
        """

        return getattr(self, 'formatters', None)

    def format_value(self, field, instance):
        """ Format a given field name and instance with defined formatter
        if a formatter is defined for the specific field. This method
        is added to the context for use in a template, for example::

            {% for object in objects %}
                {% for column in columns %}
                    {{ format_value(column, object) }}
                {% endfor %}
            {% endfor %}

        Arguments
        ---------
        field : str
            Field name on model
        instance : obj
            Instance of model

        Returns
        -------
        anything
            Formatted value
        """

        formatters = self.get_formatters()

        try:
            value = getattr(instance, field)
        except AttributeError:
            return 'Invalid Attribute: {0}'.format(field)

        if formatters:
            formatter = formatters.get(field)
            if formatter:
                value = formatter(value)

        return value


class ObjectMixin(SingleObjectMixin):
    """ Mixin for returning a single object.

    See Also
    --------
    * :py:class:`flask_velox.mixins.sqla.object.SingleObjectMixin`
    """

    def set_context(self):
        """ Set the context for a Object view.

        See Also
        --------
        * :py:meth:`from flask_velox.mixins.context.ContextMixin.set_context`

        Note
        ----
        Adds the following context variables.

        * ``object``: List of columns
        """

        super(ObjectMixin, self).set_context()

        self.add_context(self.get_object_context_name(), self.get_object())

    def get_object_context_name(self):
        """ Returns the context name to use for returning the object to the
        template, defaults to ``object``.

        Returns
        -------
        str
            Context name to use for object in template
        """

        return getattr(self, 'object_context_name', 'object')
