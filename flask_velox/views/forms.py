# -*- coding: utf-8 -*-

""" Module provides views for basic form rendering and processing.

Note
----
The following packages must be installed:

* ``Flask-WTF``
"""

from flask_velox.mixins.forms import FormMixin, MultiFormMixin


class FormView(FormMixin):
    """ Class implements :py:class:`flask_velox.mixins.forms.FormMixin`
    allowing rendering of ``Flask-WTF`` forms.

    Note
    ----
    Context pased to template:

    * ``form``: The instantiated form class
    * ``submit_url_rule``: Raw flask url rule
    * ``submit_url``: Function to call to generate the submit url for the form

    Example
    -------

    .. code-block:: python

        from flask.ext.velox.views.forms import FormView
        from yourapp.forms import MyForm

        class MyView(FormView):
            template = 'form.html'
            form = MyForm
    """

    pass


class MultiFormView(MultiFormMixin):
    """ Class implements :py:class:`flask_velox.mixins.forms.MultiFormMixin`
    allowing rendering of multiple ``Flask-WTF`` forms.

    Note
    ----
    Context pased to template:

    * ``forms``: The instantiated form classes
    * ``submit_url_rule``: Raw flask url rule
    * ``submit_url``: Function to call to generate the submit url for the form

    Example
    -------

    .. code-block:: python

        from flask.ext.velox.views.forms import MultiFormView
        from yourapp.forms import FooForm, BarForm

        class MyView(MultiFormView):
            template = 'forms.html'
            forms = [FooForm, BarForm]
    """

    pass
