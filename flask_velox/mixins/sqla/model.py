# -*- coding: utf-8 -*-

"""
Module provides mixin classes for dealing with SQLALchemy models

Note
----
Flask SQLAlchemy must be installed

Example
-------

>>> from flask.ext.velox.mixins.sqla.model import ModelMixin
>>> from yourapp import db
>>> from yourapp.models import SomeModel
...
>>> app = Flask(__name__)
...
>>> class MyView(ModelMixin):
...     session = db.session
...     model = SomeModel

"""

from flask import request


class BaseModelMixin(object):
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


class ListModelMixin(BaseModelMixin):
    """ Mixin provides ability to list multiple instances of a SQLAlchemy
    model.

    As well as attributes supported by the classes this mixin inherits from
    other attributes are supported as well.

    Example
    -------
    >>> from flask.ext.velox.mixins.sqla.model import ListModelMixin
    >>> from yourapp import db
    >>> from yourapp.models import SomeModel
    ...
    >>> class MyView(ListModelMixin):
    ...     session = db.session
    ...     model = SomeModel
    ...     base_query = SomeModel.query.filter(foo='bar')

    Attributes
    ----------
    base_query : object, optional
        A SQLAlchemy base query object, if defined this will be used instead
        of ``self.model.query.all()``
    paginate : bool, optional
        Paginate the records using SQLAlchemy ``query.paginate``
    per_page : int, optional
        If ``paginate`` is ``True`` customise the number of records to show
        per page, defaults to ``30``
    """

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

        if getattr(self, 'paginate', False):
            page = self.get_page()
            pagination = query.paginate(page, per_page=self.get_per_page())

            return pagination.items, pagination

        return query.all(), None
