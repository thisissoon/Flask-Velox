# -*- coding: utf-8 -*-

"""
Module provides classes for rendering templates using Flask `MethodView`.

Example
-------

.. code-block:: python
    :linenos:

    from flask import Flask
    from flask.ext.velox.views.template import TemplateView
    from flask.views import MethodView

    app = Flask(__name__)

    class HomeView(TemplateView):
        template = 'templates/home.html'
        context = {
            'hello': 'word'
        }

    app.add_url_rule('/', view_func=HomeView.as_view('home'))

    app.run()

"""

from flask_velox.mixins.context import ContextMixin
from flask_velox.mixins.template import TemplateMixin


class TemplateView(ContextMixin, TemplateMixin):
    """ Renders a template with optionl context.

    Attributes
    ----------
    template : str
        Relative template path, e.g: ``templates/home.html``
    context : dict, optional
        Default context to use when rendering the template

    Example
    -------

    .. code-block:: python
        :linenos:

        class HomeView(TemplateView):
            template = 'templates/home.html'
            context = {
                'hello': 'word'
            }

    """

    pass
