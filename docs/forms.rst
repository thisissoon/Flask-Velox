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
        redirect_url_rule = 'some.rule'

The view above when called will render the ``form.html`` template, this is
something you have to make yourself. The view will also pass the following
context to the template:

* ``form``: The instantiated form class
* ``submit_url_rule``: By default this will be the views current endpoint
* ``submit_url``: A function to call in the template which generates the url

Remember you are inheriting existing provided functionality which means you
can easily customise it by overriding methods, examples below.

Example Template
~~~~~~~~~~~~~~~~

Here is how you might write a template for the above view. This assumes the
current url rule is ``forms.foo`` which relates to url ``/forms/foo``.

.. code-block:: html

    <form action={{ submit_url(foo='bar') }} method="POST">
        <ul>
            {% for field in form %}
            <li>{{ field.label }} {{ field }}</li>
            {% endfor %}
        </ul>
        <button type="submit">Submit</button>
    </form>

In the above template the generated submit url would be ``/forms/foo?foo=bar``.

Success Callback
~~~~~~~~~~~~~~~~

If a form has successfully validated a call back function will be called. By
default all this function does is issue a redirect. If you wish to alter
this behaviour you can simply override the method:

.. code-block:: python

    class MyFormView(forms.FormView):
        ...

        def success_callback(self):
            form = self.get_form()
            # Do what ever you want

Redirect URL
~~~~~~~~~~~~

Ofcourse you can also override the method use for generating the
``redirect_url`` as well, for example:

.. code-block:: python

    class MyFormView(forms.FormView):
        ...

        def success_callback(self):
            form = self.get_form()
            # Do what ever you want
            super(MyFormView, self).success_callback()  # Triggers redirect

        def redirect_url(self, **kwargs):
            return url_for('some.rule', foo='bar')
