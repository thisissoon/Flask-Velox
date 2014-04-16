# -*- coding: utf-8 -*-

""" Views for deleting objects from databases using SQLAlchemy

Note
----
The following packages must be installed:

* Flask-SQLAlchemy
"""

from flask_velox.mixins.sqla.delete import DeleteObjectMixin


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
