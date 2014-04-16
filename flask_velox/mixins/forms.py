# -*- coding: utf-8 -*-

""" Mixin classes for handeling form rendering and processing.

Note
----
Flask-WTForms must be installed
"""

from flask import request, url_for
from werkzeug.routing import RequestRedirect


class FormMixin(object):
    """ Mixin adds support for from rendering and validation.

    Example
    -------

    .. code-block:: python
        :linenos:

        from flask.velox.mixins.forms import FormMixin
        from yourapp.forms import MyForm

        class MyView(FormMixin):
            form_class = MyForm

    Attributes
    ----------
    form_class : class
        An uninstantiated WTForm class
    redirect_url_rule : str
        Raw Flask url rule, e.g: 'some.url.rule'
    submit_url_rule : str, optional
        Flask url rule for form submit action e.g: 'some.url.rule'
    """

    def get_submit_url_rule(self):
        """ Returns a submit url rule for usage in generating a submit form
        action url. Defaults to the views current url rule endpoint but can be
        overridden by defining ``submit_url_rule`` on the view class.abs

        Returns
        -------
        str:
            Raw flask url rule endpoint
        """

        return getattr(self, 'submit_url_rule', request.url_rule.endpoint)

    def get_submit_url(self, **kwargs):
        """ Returns the url to a submit endpoint, this is used to render a link
        in forms actions::

            <form action="{{ submit_url() }}" method="POST">
            ...
            </form>

        See Also
        --------
        * :py:meth:`get_submit_url_rule`

        Arguments
        ---------
        \*\*kwargs
            Arbitrary keyword arguments passed to ``Flask.url_for``

        Returns
        -------
        str or None
            Generated url
        """

        rule = self.get_submit_url_rule()
        return url_for(rule, **kwargs)

    def get_form_class(self):
        """ Returns defined ``form_class`` or riases NotImplementedError

        Returns
        -------
        class
            Uninstantiated WTForm class

        Raises
        ------
        NotImplementedError
            If ``form_class`` is not defined
        """

        try:
            return self.form
        except AttributeError:
            raise NotImplementedError('``form`` must be defined')

    def success_callback(self):
        """ Called on successful form validation, by default this will perform
        a redirect if ``redirect_url_rule`` is defined. Override this method
        to perform any custom actions on successful form validation.

        Returns
        -------
        werkzeug.wrappers.Response
            Redirects request to somewhere else

        Raises
        ------
        NotImplementedError
            If ``redirect_url_rule`` is not defined
        """

        try:
            rule = self.redirect_url_rule
        except AttributeError:
            raise NotImplementedError('``redirect_url_rule`` required.')

        raise RequestRedirect(url_for(rule))

    def instantiate_form(self):
        """ Instantiates form if instance does not already exisst. Override
        this method to tailor form instantiation.

        Returns
        -------
        object
            Instantiated form
        """

        return self.get_form_class()()

    def get_form(self):
        """ Returns an instantiated WTForm class.

        Returns
        -------
        object:
            Instantiated form
        """

        try:
            return self._form
        except AttributeError:
            self._form = self.instantiate_form()
            if self._form.validate_on_submit():
                return self.success_callback()
            return self._form
