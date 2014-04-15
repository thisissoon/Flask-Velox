# -*- coding: utf-8 -*-

""" Module provides Views for handling CRUD actions on SQLAlchemy models
using Flask-WTForms.

Note
----
Requires the following packages are installed:

* Flask-SQLAlchemy
* Flask-WTForms
"""

from flask_velox.mixins.context import ContextMixin
from flask_velox.mixins.template import TemplateMixin
from flask_velox.mixins.sqla.forms import (
    CrateModelFormMixin)


class CreateModelView(CrateModelFormMixin, ContextMixin, TemplateMixin):
    """
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
            model = MyMod
            form = MyForm
    """

    methods = ['GET', 'POST', ]

    def __init__(self, *args, **kwargs):
        """ Constructor, performs initial project setup and adds extra
        context variables.
        """

        super(CreateModelView, self).__init__(*args, **kwargs)

        self.merge_context({
            'form': self.get_form(),
            'model': self.get_model()
        })

        try:
            from flask.ext.wtf.form import _is_hidden
            self.add_context('is_hidden_field', _is_hidden)
        except ImportError:
            pass
