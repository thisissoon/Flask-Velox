# -*- coding: utf-8 -*-

""" Mixin classes for helping build forms with WTForms populating SQLAlchemy
objects.

Note
----
The following packages must be installed:

* Flask-WTF
* Flask-SQLAlchemy
"""

from flask import flash
from flask_velox.mixins.forms import FormMixin, MultiFormMixin
from flask_velox.mixins.sqla.object import SingleObjectMixin


class BaseCreateUpdateMixin(object):
    """ Base Mixin for Creating or Updating a object with SQLAlchemy.

    Warning
    -------
    This mixin cannot be used on it's own and should be used inconjunction
    with others, such as :py:class:`ModelFormMixin`.
    """

    def success_callback(self):
        """ Overrides ``success_callback`` creating new model objects. This
        method is called on successful form validations. It first obtains
        the current db session and the instantiated form. A blank object
        is obtained from the model and then populated with the form data.

        .. literalinclude:: ../../../../flask_velox/mixins/sqla/forms.py
            :language: python
            :emphasize-lines: 5
            :lines: 49-56

        See Also
        --------
        * :py:meth:`flask_velox.mixins.forms.BaseFormMixin.success_callback`

        Returns
        -------
        werkzeug.wrappers.Response
            Redirects request to somewhere else
        """

        session = self.get_session()
        form = self.get_form()
        obj = self.get_object()

        form.populate_obj(obj)

        session.add(obj)
        session.commit()

        self.flash()

        return super(BaseCreateUpdateMixin, self).success_callback()


class CreateModelFormMixin(
        SingleObjectMixin,
        BaseCreateUpdateMixin,
        FormMixin):
    """ Handles creating objects after form validation has completed and
    was successful.
    """

    def flash(self):
        """ Flash created message to user.
        """

        flash('Successfully created {0}'.format(self.get_object()), 'success')


class UpdateModelFormMixin(
        SingleObjectMixin,
        BaseCreateUpdateMixin,
        FormMixin):
    """ Handels updating a single existing object after form validation has
    completed and was successful.
    """

    def flash(self):
        """ Flash updated message to user.
        """

        flash('Successfully updated {0}'.format(self.get_object()), 'success')

    def instantiate_form(self, **kwargs):
        """ Overrides form instantiation so object instance can be passed
        to the form.

        .. literalinclude:: ../../../../flask_velox/mixins/sqla/forms.py
            :language: python
            :emphasize-lines: 4
            :lines: 112-116

        See Also
        --------
        * :py:class:`flask_velox.mixins.sqla.object.SingleObjectMixin`
        * :py:meth:`flask_velox.mixins.forms.BaseFormMixin.instantiate_form`

        Returns
        -------
        object
            Instantiated form
        """

        obj = self.get_object()

        return super(UpdateModelFormMixin, self).instantiate_form(
            obj=obj,
            **kwargs)


class UpdateModelMultiFormMixin(
        SingleObjectMixin,
        BaseCreateUpdateMixin,
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
