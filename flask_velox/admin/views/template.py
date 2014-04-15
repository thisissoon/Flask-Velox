# -*- coding: utf-8 -*-

"""
Module provides classes for integrating ``Flask-Velox`` Views with
``Flask-Admin``.
"""

from flask_velox.views.template import TemplateView
from flask_velox.admin.mixins.template import AdminTemplateMixin


class AdminTemplateView(TemplateView, AdminTemplateMixin):
    """ Overrides default ``TemplateView`` methods to provide admin
    render functionality.

    Note
    ----
    * Flask-Admin must be installed
    * Overrides :py:class:`flask_velox.views.template.TemplateView`

    Example
    -------

    .. code-block:: python
        :linenos:

        from flask import Flask
        from flask.ext.admin import Admin, BaseView, expose_pluggable
        from flask.ext.velox.admin.views import AdminTemplateView

        app = Flask(__name__)
        admin = Admin(app)

        class AdminIndexView(BaseView):

            @expose_pluggable('/')
            class index(AdminTemplateView):
                template = 'admin/index.html'

        admin.add_view(AdminIndexView(name='index'))
        app.run()

    """

    pass
