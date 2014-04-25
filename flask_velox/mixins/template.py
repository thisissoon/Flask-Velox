# -*- coding: utf-8 -*-

"""
Module provides mixins for rendering templates using Flask `MethodView`.

Example
-------

.. code-block:: python
    :linenos:

    from flask import Flask
    from flask.ext.velox.mixins.template import TemplateMixin
    from flask.views import MethodView

    app = Flask(__name__)

    class MyView(TemplateMixin):
        template = 'templates/home.html'

    app.add_url_rule('/', view_func=MyView.as_view('myview'))

    app.run()

"""

from flask import render_template, request
from flask.views import MethodView


class TemplateMixin(MethodView):
    """ Renders a template on HTTP GET request as long as the ``template``
    attribute is defined.

    Attributes
    ----------
    template : str
        Relative template path, e.g: ``templates/home.html``

    Example
    -------

    .. code-block:: python
        :linenos:

        class MyView(TemplateMixin):
            template = 'templates/home.html'

    """

    def __getattr__(self, name):
        """ Overriding this allows us to access request view args as attributes
        on view instances.

        Returns
        -------
        anything
            Attribute value

        Raises
        ------
        AttributeError
            If attribute does not exist
        """

        if not hasattr(self, '_view_args'):
            self._view_args = request.view_args

        val = request.view_args.get(format(name))

        if not val:
            return super(TemplateMixin, self).__getattribute__(name)

        return val

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

    def render(self):
        """ Renders a template. This method will attempt to pass context
        to the template but if the ``context`` attribute does not exist then
        an empty dict will be passed to the ``render_template`` method.

        Returns
        -------
        str
            Rendered template

        """

        # See if we have a get_context method, if not return a blank
        # context dict
        get_context = getattr(self, 'get_context', lambda: {})

        return render_template(
            self._template,
            **get_context())

    def get(self, *args, **kwargs):
        """ Handle HTTP GET requets using Flask ``MethodView`` rendering a
        single html template.

        Returns
        -------
        str
            Rendered template

        """

        return self.render()
