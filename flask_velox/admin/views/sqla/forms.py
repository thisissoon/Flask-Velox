# -*- coding: utf-8 -*-

"""
Module provides classes for rendering views / forms for SQLAlchemy based models
within ``Flask-Admin`` systems.

Note
----
The following packages must be installed.

* Flask-SQLAlchemy
* Flask-WTForms
* Flask-Admin
"""

from flask_velox.admin.mixins.template import AdminTemplateMixin
from flask_velox.views.sqla.forms import CreateModelView


class AdminCreateModelView(AdminTemplateMixin, CreateModelView):

    template = 'admin/forms/create.html'
