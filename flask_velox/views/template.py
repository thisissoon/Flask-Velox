# -*- coding: utf-8 -*-

"""
Module provides classes for rendering templates using Flask `MethodView`.

Example
-------

>>> from flask import Flask
... from flask.ext.velox.views.template import TemplateView
... from flask.views import MethodView
...
... app = Flask(__name__)
...
... class HomeView(TemplateView):
...     template = 'templates/home.html'
...
... app.add_url_rule('/', view_func=HomeView.as_view('home'))
...
... app.run()

"""

from flask import render_template
from flask.views import MethodView


class TemplateView(MethodView):
    """ Renders a template on HTTP GET request as long as the ``template``
    attribute is defined.

    Attributes
    ----------
    template : str
        Relative template path, e.g: ``templates/home.html``

    Example
    -------
    >>> class HomeView(TemplateView):
    ...     template = 'templates/home.html'

    """

    @property
    def _template(self):
        """ Returns the defined template which should be set using the
        ``template`` attribute on classes inheriting this view.

        Returns
        -------
        str
            Relative template path, e.g: ``templates/home.html``

        Raises
        ------
        NotImplementedError
            If ``self.template`` attribute is not defined

        """

        try:
            return self.template
        except AttributeError:
            raise NotImplementedError('template attribute is not defined')

    def get(self):
        """ Handle HTTP GET requets using Flask ``MethodView`` rendering a
        single html template.

        Returns
        -------
        str
            Rendered template

        """

        return render_template(self._template)
