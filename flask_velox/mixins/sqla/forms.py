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
from flask_velox.mixins.forms import FormMixin
from flask_velox.mixins.sqla.object import SingleObjectMixin


class ModelFormMixin(SingleObjectMixin, FormMixin):
    """ Extends functionality provided by
    :py:class:`flask_velox.mixins.forms.FormMixin` allowing for
    SQLAlchemy model objects to be populated.

    Example
    -------

    .. code-block:: python
        :linenos:

        from flask.ext.velox.mixins.sqla.forms import ModelFormMixin
        from yourapp.forms import MyForm
        from yourapp.models import MyModel

        class MyView(ModelFormMixin):
            model = MyModel
            form_class = MyForm
    """

    pass


class CrateModelFormMixin(ModelFormMixin):
    """ Handles creating objects after form validation has completed and
    was successful.
    """

    def success_callback(self):
        """ Overrides ``success_callback`` creating new model objects

        See Also
        --------
        :py:meth:`flask_velox.mixins.forms.FormMixin.success_callback`

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

        return super(CrateModelFormMixin, self).success_callback()


class UpdateModelFormMixin(ModelFormMixin):
    """ Handels updating existing objects with form data.
    """

    def success_callback(self):
        """ Overrides ``success_callback`` updating existing object

        See Also
        --------
        :py:meth:`flask_velox.mixins.forms.FormMixin.success_callback`

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

        return super(UpdateModelFormMixin, self).success_callback()
