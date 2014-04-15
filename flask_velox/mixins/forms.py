# -*- coding: utf-8 -*-

""" Mixin classes for handeling form rendering and processing.

Note
----
Flask-WTForms must be installed
"""


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
    """

    def get_form(self):
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
            return self.form_class
        except AttributeError:
            raise NotImplementedError('``form_class`` must be defined')

    def form(self):
        """ Returns an instantiated WTForm class.

        Returns
        -------
        object:
            Instantiated form
        """

        pass
