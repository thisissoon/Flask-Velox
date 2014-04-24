Forms
=====

``Flask-Velox`` comes with SQLAlchemy form integration to hopefully make
those Create / Update tasks as simple as possible.

.. note::
    The following packages must be installed:

    * ``Flask-SQLAlchemy``
    * ``Flask-WTF``

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

Update View
-----------

.. _`WTForms-Alchemy`: http://wtforms-alchemy.readthedocs.org/en/latest/
