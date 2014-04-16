# -*- coding: utf-8 -*-

""" Views for deleting objects from databases using SQLAlchemy

Note
----
The following packages must be installed:

* Flask-SQLAlchemy
"""

from flask_velox.mixins.sqla.delete import (
    DeleteObjectMixin,
    MultiDeleteObjectMixin)


class DeleteObjectView(DeleteObjectMixin):
    """ View for deleting single objects from databases using SQLAlchemy.

    Example
    -------

    .. code-block:: python
        :linenos:

        from flask.ext.velox.views.sqla.delete import DeleteObjectView
        form yourapp import db
        from yourapp.models import MyModel

        class MyView(DeleteObjectView):
            template = 'delete.html'
            model = MyModel
            session = db.session

    """

    pass


class MultiDeleteObjectView(MultiDeleteObjectMixin):
    """ View for deleting multiple objects from databases using SQLAlchemy.

    Example
    -------

    .. code-block:: python
        :linenos:

        from flask.ext.velox.views.sqla.delete import MultiDeleteObjectView
        form yourapp import db
        from yourapp.models import MyModel

        class MyView(MultiDeleteObjectView):
            template = 'delete.html'
            model = MyModel
            session = db.session

    Attributes
    ----------
    methods : list
        Allowed HTTP method verbs, defaults to ``['GET', 'POST', ]``
    """

    #: Allowed HTTP Methods
    methods = ['GET', 'POST', ]

    def post(self, *args, **kwargs):
        """ Handle HTTP POST requests rendering a template.
        """

        return self.render()
