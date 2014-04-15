""" Mixin classes specific to ``Flask-Admin`` and ``Flask-SQLAlchemy``
based views.

Note
----
``Flask-Admin`` Must be installed
``Flask-SQLAlchemy`` Must be installed
"""

from flask import url_for
from flask_velox.mixins.sqla.model import TableModelMixin


class AdminTableModelMixin(TableModelMixin):
    """ Extends the default functionality of
    :py:class:`flask_velox.mixins.sqla.model.TableModelMixin` adding admin
    specific functionality, for example the ability to add CRUD urls so the
    table can render links to other views.

    Example
    -------
    .. code-block:: python
        :linenos:

        from yourapp.models import MyModel
        class MyView(AdminTableModelMixin):
            model = MyModel
            create_url_rule = 'admin.mymodel.create'
            update_url_rule = 'admin.mymodel.update'
            delete_url_rule = 'admin.mymodel.delete'
            with_selected = {
               'Delete': 'admin.mymodel.delete',
            }

    Note
    ----
    The Flask URL Rules shown above are dependant on how the admin class
    is registered. In this case it would be registered with an ``endpoint``
    key word argument, for example::

        MyView(
            name='My Model',
            url='mymodel',
            endpoint='admin.mymodel')

    Attributes
    ----------
    create_url_rule : str
        Flask url rule for linkinging to create views for the model
    update_url_rule : str
        Flask url rule for linkinging to update views for the model
    delete_url_rule : str
        Flask url rule for linkinging to delete views for the model
    with_selected : dict
        Dictionary containg a human name as the key and a Flask url rule
        as the value. In the example below ``Delete`` is the name which will
        appear in the ``With Selected`` with the url being the destination
        of the link.
    """

    def get_create_url_rule(self):
        """ Returns the ``create_url_rule`` or None if not defined.

        Returns
        -------
        str or None
            Defined ``create_url_rule`` or None
        """

        return getattr(self, 'create_url_rule', None)

    def get_update_url_rule(self):
        """ Returns the ``update_url_rule`` or None if not defined.

        Returns
        -------
        str or None
            Defined ``update_url_rule`` or None
        """

        return getattr(self, 'update_url_rule', None)

    def get_delete_url_rule(self):
        """ Returns the ``delete_url_rule`` or None if not defined.

        Returns
        -------
        str or None
            Defined ``delete_url_rule`` or None
        """

        return getattr(self, 'delete_url_rule', None)

    def get_with_selected(self):
        """ Just returns the value of ``with_selected`` or None of not
        defined.

        Returns
        -------
        dict or None
            Values of ``with_selcted``
        """

        return getattr(self, 'with_selected', None)

    def create_url(self, **kwargs):
        """ Returns the url to a create endpoint, this is used to render a link
        in admin table views with the destination of this url, should be added
        to view context and called in the template::

            <a href="{{ create_url() }}">Create New</a>

        The ``create_url_rule`` must be defined otherwise None will be
        returned.

        Arguments
        ---------
        \*\*kwargs
            Arbitrary keyword arguments passed to ``Flask.url_for``

        Returns
        -------
        str or None
            Generated url or None
        """

        rule = getattr(self, 'create_url_rule', None)
        if rule:
            return url_for(rule, **kwargs)

        return None

    def update_url(self, pk, **kwargs):
        """ Returns the url for updating a specific record, this method
        needs to be passed to the context of the view so it can be used
        in the template, for example::

            {% for object in objects %}
                <a href="{{ update_url(object.id) }}">Update</a>
            {% endfor %}

        If ``update_url_rule`` is not defined ``None`` will be returned.

        Arguments
        ---------
        pk : any
            Object primary key, could be any type
        \*\*kwargs
            Arbitrary keyword arguments passed to ``Flask.url_for``

        Returns
        -------
        str or None
            Generated url or None
        """

        rule = getattr(self, 'update_url_rule', None)
        if rule:
            return url_for(rule, pk=pk, **kwargs)

        return None

    def delete_url(self, pk, **kwargs):
        """ Returns the url for deleting a specific record, this method
        needs to be passed to the context of the view so it can be used
        in the template, for example::

            {% for object in objects %}
                <a href="{{ delete_url(object.id) }}">Delete</a>
            {% endfor %}

        If ``delete_url_rule`` is not defined ``None`` will be returned.

        Arguments
        ---------
        pk : any
            Object primary key, could be any type
        \*\*kwargs
            Arbitrary keyword arguments passed to ``Flask.url_for``

        Returns
        -------
        str or None
            Generated url or None
        """

        rule = getattr(self, 'delete_url_rule', None)
        if rule:
            return url_for(rule, pk=pk, **kwargs)

        return None
