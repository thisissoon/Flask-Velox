Quickstart
==========

``Flask-Velox`` is designed to be quick to use and easy to extend. Here you
will see some basic examples of what ``Flask-Velox`` can do.

Concept
-------

The idea behind ``Flask-Velox`` was to write a set of classes which can be
mixed in together to build easily implimentable Flask `MethodView`_ pluggable
views which could be used on the public and private admin systems.

.. seealso::

    * Flask `MethodView`_

In ``Flask-Velox`` the mixin classes are king and they do all the hard work
and heavy lifting, Views simply implement these mixin classes, you can see a
full set of mixin classes in the :doc:`api`.

This approach allows us to easily implement Views of various mixin
configuration and create views for admin systems just as quickly.

Template View
-------------

The most common task any web application will need is to render a HTML
document. The  class is ``TemplateMixin`` the core class which almost all other
views will implement in order to render a page of HTML. The ``TemplateView``
class is the simplest view which implements the ``TemplateMixin`` as well as
the ``ContextMixin`` allowing us to pass context to our template.

.. seealso::

    * :py:class:`flask_velox.mixins.context.ContextMixin`
    * :py:class:`flask_velox.mixins.template.TemplateMixin`
    * :py:class:`flask_velox.views.template.TemplateView`

Take this example:

.. code-block:: python

    from flask import Flask
    from flask.ext.velox import Velox
    from flask.ext.velox.views.template import TemplateView

    app = Flask(__name__)

    velox = Velox()
    velox.init_app(app)

    class HomeView(TemplateView):
        template = 'home.html'
        context = {
            'foo': 'bar'
        }

    app.add_url_rule('/', view_func=HomeView.as_view('home'))

    app.run()

The above example creates a ``HomeView`` class which extends the
``TemplateView`` which implements the ``TemplateMixin`` and ``ContextMixin``.
The View defines the template to render and some default context to use
when rendering the template. All other bundled views with ``Flask-Velox``
follow a similar pattern.

.. _`MethodView`: http://flask.pocoo.org/docs/views/#method-based-dispatching
