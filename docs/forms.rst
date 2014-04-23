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

.. code-block:: html+jinja

    <form action="{{ submit_url(foo='bar') }}" method="POST">
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

Multi Form View
---------------

Sometimes you want to render multiple forms on a page, this can be done with
``Flask-Velox`` by extending the ``MultiFromView`` like so:

.. code-block:: python

    from flask.ext.velox.views import forms
    from yourapp.forms import FooForm, BarForm

    class MyFormView(forms.MultiFormView):
        template = 'forms.html'
        forms = [
            ('Foo', FooForm)
            ('Bar', BarForm)
        ]
        redirect_url_rule = 'some.rule'

Here we have defined ``forms`` to contain a list of form classes, the rest is
the same as a regular ``FormView``.

The following context is returned:

* ``forms``: Dict of instantiated form classes
* ``submit_url_rule``: By default this will be the views current endpoint
* ``submit_url``: A function to call in the template which generates the url.

As with the ``FormView`` you can override behaviour by overriding methods:

.. code-block:: python

    class MyFormView(forms.MultiFormView):
        ...

        def submit_url(self, **kwargs):
            return url_for('some.rule', foo='bar')

Example Template
~~~~~~~~~~~~~~~~

When rending a template for multi form views its important to understand
what the ``forms`` context contains::

    {
        'form1': ('Foo', form),
        'form2': ('Bar', form)
    }

The ``forms`` context variable is a dict where the key represents a form id
and the value containing the name of the form and the instantiated form class.

Here is an example template:

.. code-block:: html+jinja
    :linenos:
    :emphasize-lines: 5

    {% for id, data in forms.iteritems() %}
    {% set name, form = data %}
    <h2>{{ name }}</h2>
    <form action="{{ submit_url(foo='bar') }}" method="POST" id="{{ id }}">
        <input type="hidden" name="form" id="form" value="{{ id }}">
        <ul>
            {% for field in form %}
            <li>{{ field.label }} {{ field }}</li>
            {% endfor %}
        </ul>
        <button type="submit">Submit</button>
    </form>
    {% endform %}

Line 5 is emphasized as we have added a hidden field containing the form id
which is generated at run time, its this which is used to determine which
form has been submit and therefore which needs to validated.

Success Callback
~~~~~~~~~~~~~~~~

In a multi form view only one form can be submit at a time, this means the
behaviour of the ``get_form`` method will have changed, it will now only return
the submit form object.

.. code-block:: python

    class MyFormView(forms.MultiFormView):
        ...

        def success_callback(self):
            form = self.get_form()  # The submit form and is valid
            # Do what ever you want
