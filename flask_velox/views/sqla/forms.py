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
    CrateModelFormMixin,
    UpdateModelFormMixin)


class BaseModelView(ContextMixin, TemplateMixin):
    """
    """

    methods = ['GET', 'POST', ]

    def set_context(self):
        """ Overrides ``set_context`` to set extra context variables.

        See Also
        --------
        * :py:meth:`from flask_velox.mixins.context.ContextMixin.set_context`
        """

        super(BaseModelView, self).set_context()

        self.merge_context({
            'form': self.get_form(),
            'model': self.get_model()
        })

        try:
            from flask.ext.wtf.form import _is_hidden
            self.add_context('is_hidden_field', _is_hidden)
        except ImportError:
            pass

    def post(self, *args, **kwargs):
        """ Handle HTTP POST requets using Flask ``MethodView`` rendering a
        single html template.

        Returns
        -------
        str
            Rendered template
        """

        return self.render()


class CreateModelView(CrateModelFormMixin, BaseModelView):
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
            model = MyMod
            form = MyForm
    """

    pass


class UpdateModelFormMixin(UpdateModelFormMixin, BaseModelView):
    """ View for creating new model objects.

    Example
    -------

    .. code-block:: python
        :linenos:

        from flask.ext.velox.views.sqla.forms import UpdateModelView
        from yourapp import db
        from yourapp.forms import MyForm
        from yourapp.models import MyModel

        class MyView(UpdateModelView):
            template = 'create.html'
            session = db.session
            model = MyMod
            form = MyForm
    """

    pass
