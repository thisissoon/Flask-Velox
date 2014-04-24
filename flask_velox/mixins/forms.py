# -*- coding: utf-8 -*-

""" Mixin classes for handeling form rendering and processing.

Note
----
The following packages must be installed:

* Flask-WTF
"""

from collections import OrderedDict
from flask import request, url_for
from flask_velox.mixins.context import ContextMixin
from flask_velox.mixins.template import TemplateMixin
from werkzeug.routing import RequestRedirect


class BaseFormMixin(ContextMixin, TemplateMixin):
    """ Base Form Mixin class, defines some standard methods required for
    both single and multi forms.

    Attributes
    ----------
    redirect_url_rule : str
        Raw Flask url rule, e.g: ``some.url.rule``
    submit_url_rule : str, optional
        Flask url rule for form submit action e.g: 'some.url.rule'
    """

    def flash(self):
        """ Override this method to call a flask flash method. By default this
        method does nothing.

        Example
        -------

        .. code-block:: python

            class MyView(FromMixin):
                form = Form

                def flash(self):
                    flash('Message', 'success')
        """

        pass

    def set_context(self):
        """ Overrides ``set_context`` to set extra context variables.

        See Also
        --------
        * :py:meth:`from flask_velox.mixins.context.ContextMixin.set_context`

        Note
        ----
        Adds the following extra context variables:

        * ``is_hidden_field``: Function for determining is field is hidden
        """

        super(BaseFormMixin, self).set_context()

        self.merge_context({
            'submit_url_rule': self.get_submit_url_rule(),
            'submit_url': self.submit_url
        })

        try:
            from flask.ext.wtf.form import _is_hidden
            self.add_context('is_hidden_field', _is_hidden)
        except ImportError:
            pass

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

    def get_redirect_url_rule(self):
        """ Returns raw redirect url rule to be used in ``url_for``. The
        ``redirect_url_rule`` must be defined else NotImplementedError will
        be raised.

        Returns
        -------
        str
            Raw flask url endpoint

        Raises
        ------
        NotImplementedError
            If ``redirect_url_rule`` is not defined
        """

        try:
            return self.forms
        except AttributeError:
            raise NotImplementedError('``redirect_url_rule`` must be defined.')

    def submit_url(self, **kwargs):
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

    def redirect_url(self, **kwargs):
        """ Returns the url to a redirect endpoint, when the form is valid
        and the callback is called.

        See Also
        --------
        * :py:meth:`get_redirect_url_rule`

        Arguments
        ---------
        \*\*kwargs
            Arbitrary keyword arguments passed to ``Flask.url_for``

        Returns
        -------
        str or None
            Generated url
        """

        rule = self.get_redirect_url_rule()
        return url_for(rule, **kwargs)

    def instantiate_form(self, kls=None, obj=None, prefix=''):
        """ Instantiates form if instance does not already exisst. Override
        this method to tailor form instantiation.

        Arguments
        ---------
        kls : class, optional
            Form class to instantiate, defaults to None
        obj : object, optional
            Object to pass into the form to pre populate with
        prefix : str, optional
            Add a prefix to the form class

        Returns
        -------
        object
            Instantiated form
        """

        if kls:
            return kls(obj=obj, prefix=prefix)

        return self.get_form_class()(obj=obj, prefix=prefix)

    def success_callback(self):
        """ Called on successful form validation, by default this will perform
        a redirect if ``redirect_url_rule`` is defined. Override this method
        to perform any custom actions on successful form validation.

        Returns
        -------
        werkzeug.wrappers.Response
            Redirects request to somewhere else
        """

        raise RequestRedirect(self.redirect_url())

    def post(self, *args, **kwargs):
        """ Handle HTTP POST requets using Flask ``MethodView`` rendering a
        single html template.

        Returns
        -------
        str
            Rendered template
        """

        return self.render()


class FormMixin(BaseFormMixin):
    """ Renders and validates a single Form.

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
    form : class
        An uninstantiated WTForm class
    """

    def set_context(self):
        """ Overrides ``set_context`` to set extra context variables.

        See Also
        --------
        * :py:meth:`from flask_velox.mixins.context.ContextMixin.set_context`

        Note
        ----
        Adds the following extra context variables:

        * ``form``: Instantiated form object
        """

        super(FormMixin, self).set_context()

        self.add_context('form', self.get_form())

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


class MultiFormMixin(BaseFormMixin):
    """ Mixin allows rendering of multiple forms in a single template, each
    form is submit individually and validated individually but to the same
    endpoint.

    Example
    -------

    .. code-block:: python
        :linenos:

        from flask.velox.mixins.forms import MultiFormMixin
        from yourapp.forms import Form1, Form2

        class MyView(MultiFormMixin):
            forms = [
                ('Form 1', Form1)
                ('Form 2', Form2)
            ]

    """

    def set_context(self):
        """ Updates context to contain extra variables.

        See Also
        --------
        * :py:meth:`from flask_velox.mixins.context.ContextMixin.set_context`

        Note
        ----
        Adds the following extra context variables:

        * ``forms``: List of forms

        """

        super(MultiFormMixin, self).set_context()

        self.add_context('forms', self.get_forms())

    def get_form_classes(self):
        """ Return list of tuples of form classes, the tuple should contain
        a human readable name and a form class defined in ``forms``
        attribute. If not set ``NotImplementedError`` is risen.

        Returns
        -------
        list
            Tuples containing human name and form class

        Raises
        ------
        NotImplementedError
            ``forms`` attribute is not defined
        """

        try:
            return self.forms
        except AttributeError:
            raise NotImplementedError('``forms`` must be defined.')

    def get_form(self):
        """ Get the submit form if one exists else return None, this allows
        us to get the correctly submit form to validate against and populate
        objects if required.

        A hidden field must be included in each ``<form>`` block named
        ``form`` containing the value of the forms prefix. This is the forms
        uniqie identifier and is used to obtain the submit form.

        Returns
        -------
        obj or None
            Submit form object or None if submit form not found
        """

        try:
            return self._form
        except AttributeError:
            forms = self.get_forms()
            submit_form = request.values.get('form')
            name, form = forms.get(submit_form)
            if form:
                if form.validate_on_submit():
                    self.success_callback()
                self._form = form
                return form

        return None

    def is_submit(self, form, prefix):
        """ If the form has been submit run the validate on submit method
        and call the success callback if the form is valid.

        Arguments
        ---------
        form : object
            Instantiated form object
        prefix : str
            Form prefix id

        Returns
        -------
        bool
            If the form was submit§
        """

        submit_form = request.values.get('form')
        if prefix == submit_form:
            if form.validate_on_submit():
                self._form = form
                self.success_callback()
            return True

        return False

    def get_forms(self):
        """ Instantiates forms set in ``forms`` attribute giving each form
        an individual prefix and storing each form in a ``dict`` using its
        prefix as the key.

        Returns
        -------
        collections.OrderedDict
            Instantiated forms with form prefix as key and a tuple containing
            the human readable form name and form object::

                {
                    'form1': ('Foo Form', <object>),
                    'form1': ('Bar Form', <object>)
                }
        """

        try:
            return self._forms
        except AttributeError:
            forms = OrderedDict()
            classes = self.get_form_classes()
            for i, values in enumerate(classes, start=1):
                name, kls = values
                prefix = 'form{0}'.format(i)
                form = self.instantiate_form(
                    kls=kls,
                    prefix=prefix)
                forms[prefix] = (name, form)
                self.is_submit(form, prefix)
            self._forms = forms
            return forms
