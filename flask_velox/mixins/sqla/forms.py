# -*- coding: utf-8 -*-

""" Mixin classes for helping build forms with WTForms populating SQLAlchemy
objects.

Note
----
The following packages must be installed:

* Flask-WTForms
* Flask-SQLAlchemy
"""

from flask import flash
from flask_velox.mixins.forms import FormMixin, MultiFormMixin
from flask_velox.mixins.sqla.object import SingleObjectMixin


class BaseCreateMixin(object):
    """ Base Mixin for Creating a object with SQLAlchemy.

    Warning
    -------
    This mixin cannot be used on it's own and should be used inconjunction
    with others, such as :py:class:`ModelFormMixin`.
    """

    def success_callback(self):
        """ Overrides ``success_callback`` creating new model objects

        See Also
        --------
        * :py:meth:`flask_velox.mixins.forms.FormMixin.success_callback`

        Returns
        -------
        werkzeug.wrappers.Response
            Redirects request to somewhere else

        Raises
        ------
        NotImplementedError
            If ``redirect_url_rule`` is not defined
        """

        session = self.get_session()
        form = self.get_form()
        obj = self.get_object()  # Should be a blank object

        form.populate_obj(obj)

        session.add(obj)
        session.commit()

        flash('successfully created {0}'.format(obj), 'success')

        return super(BaseCreateMixin, self).success_callback()


class BaseUpdateMixin(object):
    """ Base Mixin for Updating an object with SQLAlchemy.

    Warning
    -------
    This mixin cannot be used on it's own and should be used inconjunction
    with others, such as :py:class:`ModelFormMixin`.
    """

    def success_callback(self):
        """ Overrides ``success_callback`` updating existing object

        See Also
        --------
        * :py:meth:`flask_velox.mixins.forms.FormMixin.success_callback`

        Returns
        -------
        werkzeug.wrappers.Response
            Redirects request to somewhere else

        Raises
        ------
        NotImplementedError
            If ``redirect_url_rule`` is not defined
        """

        session = self.get_session()
        form = self.get_form()
        obj = self.get_object()  # Should be a blank object

        form.populate_obj(obj)
        session.commit()

        flash('successfully updated {0}'.format(obj), 'success')

        return super(BaseUpdateMixin, self).success_callback()

    def instantiate_form(self, **kwargs):
        """ Overrides form instantiation so object instance can be passed
        to the form.

        See Also
        --------
        * :py:meth:`flask_velox.mixins.forms.BaseFormMixin.instantiate_form`

        Returns
        -------
        object
            Instantiated form
        """

        obj = self.get_object()

        return super(BaseUpdateMixin, self).instantiate_form(
            obj=obj,
            **kwargs)


class CrateModelFormMixin(SingleObjectMixin, BaseCreateMixin, FormMixin):
    """ Handles creating objects after form validation has completed and
    was successful.
    """

    pass


class UpdateModelFormMixin(SingleObjectMixin, BaseUpdateMixin, FormMixin):
    """ Handels updating a single existing object after form validation has
    completed and was successful.
    """

    pass


class UpdateModelMultiFormMixin(
        SingleObjectMixin,
        BaseUpdateMixin,
        MultiFormMixin):
    """ Mixin for building mutli forms with a single SQAlachemy object

    Example
    -------

    .. code-block:: python
        :linenos:

        from flask.ext.velox.mixins.sqla.forms import ModelFormMixin
        from yourapp.forms import MyForm1, MyForm2
        from yourapp.models import MyModel

        class MyView(UpdateModelMultiFormMixin):
            model = MyModel
            forms = [
                'Form 1': MyForm1
                'Form 2': MyForm2
            ]

    """

    pass
