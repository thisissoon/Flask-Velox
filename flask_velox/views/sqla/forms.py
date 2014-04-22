# -*- coding: utf-8 -*-

""" Module provides Views for handling CRUD actions on SQLAlchemy models
using Flask-WTForms.

Note
----
Requires the following packages are installed:

* Flask-SQLAlchemy
* Flask-WTF
"""

from flask_velox.mixins.sqla.forms import (
    CreateModelFormMixin,
    UpdateModelFormMixin,
    UpdateModelMultiFormMixin)


class CreateModelView(CreateModelFormMixin):
    """ View for creating new model objects.

    Example
    -------

    .. code-block:: python
        :linenos:

        from flask.ext.velox.views.sqla.forms import CreateModelView
        from yourapp import db
        from yourapp.forms import MyForm
        from yourapp.models import MyModel

        class MyView(CreateModelView):
            template = 'create.html'
            session = db.session
            model = MyModel
            form = MyForm
    """

    pass


class UpdateModelFormView(UpdateModelFormMixin):
    """ View for updating model objects.

    Example
    -------

    .. code-block:: python
        :linenos:

        from flask.ext.velox.views.sqla.forms import UpdateModelView
        from yourapp import db
        from yourapp.forms import MyForm
        from yourapp.models import MyModel

        class MyView(UpdateModelView):
            template = 'update.html'
            session = db.session
            model = MyModel
            form = MyForm
    """

    pass


class UpdateModelMultiFormView(UpdateModelMultiFormMixin):
    """ View for rendering mutliple forms for a single object.

    Example
    -------

    .. code-block:: python
        :linenos:

        from flask.ext.velox.views.sqla.forms import UpdateModelView
        from yourapp import db
        from yourapp.forms import FooForm, BarForm
        from yourapp.models import MyModel

        class MyView(UpdateModelView):
            template = 'update.html'
            session = db.session
            model = MyModel
            forms = [
                ('Foo Form', FooForm),
                ('Bar Form', BarForm)
            ]
    """

    pass
