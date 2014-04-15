# -*- coding: utf-8 -*-

""" Mixin classes for handeling form rendering and processing.

Note
----
Flask-WTForms must be installed
"""

from flask import redirect, url_for


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
    """

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
            raise NotImplementedError('``form_class`` must be defined')

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

        return redirect(url_for(rule))

    def get_form(self):
        """ Returns an instantiated WTForm class.

        Returns
        -------
        object:
            Instantiated form
        """

        form = getattr(self, '_form', self.get_form_class()())
        if form.validate_on_submit():
            return self.success_callback()

        self._form = form

        return form
