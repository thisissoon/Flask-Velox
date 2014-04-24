Admin
=====

``Flask-Velox`` also has optional ``Flask-Admin`` integration which you can
use to build admin systems rapidly.

.. note::

    The following packages must be installed:

    * Flask-SQLAlchemy
    * Flask-Admin
    * Flask-WTF

How you manage authentication is up to you, ``Flask-Velox`` simply provides
views to perform standard admin tasks.

It is recommended that you view the :doc:`api` to understand the extra
attributes you can define on the admin versions of the views.

Example
-------

Using the already existing views and mixins we have created a set of admin view
classes and mixins which allow the views to be rendered within a
``Flask-Admin`` framework.

Here is a complete example which has create, read, update, delete views:

.. code-block:: python

    from flask.ext import admin
    from flask.ext.velox.admin.views.sqla import read
    from flask.ext.velox.admin.views.sqla import forms
    from flask.ext.velox.admin.views.sqla import delete
    from flask.ext.velox.formatters import datetime_formatter
    from yourapp import db
    from yourapp.forms import CreateForm, UpdateForm
    from yourapp.models import Model

    class AdminView(admin.BaseView):

        @admin.expose_plugview('/')
        class index(read.AdminModelTableView):
            model = Model
            columns = ['title', 'created', 'updated']
            formatters = {
                'created': datetime_formatter,
                'updated': datetime_formatter
            }
            with_selected = {
                'Delete': '.delete_multi',
            }

        @admin.expose_plugview('/create')
        class create(forms.AdminCreateModelView):
            model = Model
            form = CreateForm
            session = db.session

        @admin.expose_plugview('/update/<int:id>')
        class update(forms.AdminUpdateModelView):
            model = Model
            session = db.session
            form = UpdateForm

        @admin.expose_plugview('/delete/<int:id>')
        class delete(delete.AdminDeleteObjectView):
            model = Model
            session = db.session

        @admin.expose_plugview('/delete')
        class delete_multi(delete.AdminMultiDeleteObjectView):
            model = Model
            session = db.session
