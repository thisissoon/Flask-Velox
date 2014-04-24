Forms
=====

``Flask-Velox`` comes with SQLAlchemy form integration to hopefully make
those Create / Update tasks as simple as possible.

.. note::
    The following packages must be installed:

    * ``Flask-SQLAlchemy``
    * ``Flask-WTF``

.. _create-view:

Create View
-----------

The ``CreateModelView`` allows you to render a form and on successful
validation of the form creates a new object and saves to the database. You will
ofcourse need to make the form yourself, you could use `WTForms-Alchemy`_ to
automate this for you, example below:

This view is almost identical to the :ref:`Form View <form-view>` we have seen
before except that the view mixis in the ability to create an object populated
with data from the form and save that object. You can see how the success
callback function works here:

* :py:meth:`flask_velox.mixins.sqla.forms.BaseCreateUpdateMixin.success_callback`

.. code-block:: python

    from flask.ext.wtf import Form
    from flask.ext.velox.views.sqla import forms
    from wtforms import TextField
    from yourapp import db

    class MyModel(db.Model):
        field1 = db.Column(db.String(20))
        field2 = db.Column(db.String(128))

    class MyForm(Form):
        field1 = TextField()
        field2 = TextField()

    class MyCreateView(forms.CreateModelView):
        model = MyModel
        session = db.session
        form = MyForm
        template = 'create.html'

You will ofcourse need a template for rendering the form, see an
:ref:`Example Template <form-view-example-template>` in the
:ref:`Form View <form-view>` guide.

As with the :ref:`Form View <form-view>` you can override the success callback
function, redirect url etc.

.. _update-view:

Update View
-----------

The Update View follows the same principle as the :ref:`Create View
<create-view>` except that the form is instantiated with an existing object
which you can see documented here:

* :py:meth:`flask_velox.mixins.sqla.forms.UpdateModelFormMixin.instantiate_form`

.. code-block:: python

    class MyUpdateView(forms.UpdateModelView):
        model = MyModel
        session = db.session
        form = MyForm
        template = 'update.html'

Multi Form Update View
----------------------

There can sometimes be the requirement for multiple forms to update a single
object which offer different functionality, an example situation is updating
a user object where a password change form needs to be seperate from the
general user attributes form. This view allows us to do this.

Again it follows the same principles as the :ref:`create-view` and
:ref:`update-view`.

.. seealso::

    * :ref:`multi-form-view`

.. code-block:: python

    from flask.ext.velox.views.sqla import forms
    from yourapp import db
    from yourapp.forms import UserPasswordForm, UserUpdateForm
    from yourapp.models import User

    class MyMultiFormView(forms.UpdateModelMultiFormView):
        model = User
        session = db.sesion
        forms = [
            ('Change Password', UserPasswordForm)
            ('Update User', UserUpdateForm)
        ]
        template = 'mutli.html'

You can see an example template :ref:`here <multi-form-view-example-template>`.

.. _`WTForms-Alchemy`: http://wtforms-alchemy.readthedocs.org/en/latest/
