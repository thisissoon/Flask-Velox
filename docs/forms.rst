Forms
=====

Rendering forms is another core component of any web application.
``Flask-Velox`` provides views which allow us to implement ``Flask-WTF`` forms
in our views.

.. seealso::

    **Mixins**

    * :py:class:`flask_velox.mixins.forms.FormMixin`
    * :py:class:`flask_velox.mixins.forms.MultiFormMixin`

Form View
---------

The ``FormView`` class allows us to render and process a ``Flask-WTF`` form:

.. code-block:: python

    from flask.ext.velox.views import forms
    from yourapp.forms import FooForm

    class MyFormView(forms.FormView):
        template = 'form.html'
        form = FooForm
