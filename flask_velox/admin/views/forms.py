# -*- coding: utf-8 -*-

""" Module provides classes for integrating ``Flask-Velox`` Form Views with
``Flask-Admin``.

Note
----
The following packages must be installed:

* Flask-Admin
* Flask-WTForms
"""

from flask_velox.admin.mixins.template import AdminTemplateMixin
from flask_velox.mixins.forms import FormMixin


class AdminFormView(FormMixin, AdminTemplateMixin):
    """ Renders a normal form within a ``Flask-Admin`` view.
    """

    pass
