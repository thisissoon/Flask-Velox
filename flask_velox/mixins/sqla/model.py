# -*- coding: utf-8 -*-

"""
Module provides mixin classes for dealing with SQLALchemy models

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

from flask_velox.mixins.context import ContextMixin


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
