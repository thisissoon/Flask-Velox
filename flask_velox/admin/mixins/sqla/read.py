# -*- coding: utf-8 -*-

""" Mixin classes specific to ``Flask-Admin`` and ``Flask-SQLAlchemy``
based views.

Note
----
The following packages must be installed:

* ``Flask-Admin``
* ``Flask-SQLAlchemy``
"""

from flask import url_for
from flask_velox.mixins.sqla.read import TableModelMixin


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
    create_url_rule : str, optional
        Flask url rule for linkinging to create views for the model, defaults
        to ``.create``
    update_url_rule : str, optional
        Flask url rule for linkinging to update views for the model, defaults
        to ``.update``
    delete_url_rule : str, optional
        Flask url rule for linkinging to delete views for the model, defaults
        to ``.delete``
    with_selected : dict, optional
        Dictionary containg a human name as the key and a Flask url rule
        as the value. In the example below ``Delete`` is the name which will
        appear in the ``With Selected`` with the url being the destination
        of the link.
    """

    def set_context(self):
        """ Adds extra context to Admin Table Views for ``Flask-Admin``
        systems

        See Also
        --------
        * :py:meth:`from flask_velox.mixins.context.ContextMixin.set_context`

        Note
        ----
        Adds the following context variables.

        * ``create_url_rule``: The raw url rule or ``None``
        * ``create_url``: Create url method
        * ``update_url_rule``: The raw url rule or ``None``
        * ``update_url``: Update url method
        * ``delete_url_rule``: The raw url rule or ``None``
        * ``delete_url``: Delete url method
        * ``with_selcted``: With selcted values
        """

        super(AdminTableModelMixin, self).set_context()

        self.merge_context({
            'create_url_rule': self.get_create_url_rule(),
            'create_url': self.create_url,
            'update_url_rule': self.get_update_url_rule(),
            'update_url': self.update_url,
            'delete_url_rule': self.get_delete_url_rule(),
            'delete_url': self.delete_url,
            'with_selected': self.get_with_selected(),
        })

    def get_create_url_rule(self):
        """ Returns the ``create_url_rule`` or None if not defined.

        Returns
        -------
        str or None
            Defined ``create_url_rule`` or None
        """

        return getattr(self, 'create_url_rule', '.create')

    def get_update_url_rule(self):
        """ Returns the ``update_url_rule`` or None if not defined.

        Returns
        -------
        str or None
            Defined ``update_url_rule`` or None
        """

        return getattr(self, 'update_url_rule', '.update')

    def get_delete_url_rule(self):
        """ Returns the ``delete_url_rule`` or None if not defined.

        Returns
        -------
        str or None
            Defined ``delete_url_rule`` or None
        """

        return getattr(self, 'delete_url_rule', '.delete')

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

        rule = getattr(self, 'create_url_rule', '.create')
        if rule:
            return url_for(rule, **kwargs)

        return None

    def update_url(self, **kwargs):
        """ Returns the url for updating a specific record, this method
        needs to be passed to the context of the view so it can be used
        in the template, for example::

            {% for object in objects %}
                <a href="{{ update_url(id=object.id) }}">Update</a>
            {% endfor %}

        If ``update_url_rule`` is not defined ``None`` will be returned.

        Arguments
        ---------
        \*\*kwargs
            Arbitrary keyword arguments passed to ``Flask.url_for``

        Returns
        -------
        str or None
            Generated url or None
        """

        rule = self.get_update_url_rule()
        if rule:
            return url_for(rule, **kwargs)

        return None

    def delete_url(self, **kwargs):
        """ Returns the url for deleting a specific record, this method
        needs to be passed to the context of the view so it can be used
        in the template, for example::

            {% for object in objects %}
                <a href="{{ delete_url(id=object.id) }}">Delete</a>
            {% endfor %}

        If ``delete_url_rule`` is not defined ``None`` will be returned.

        Arguments
        ---------
        \*\*kwargs
            Arbitrary keyword arguments passed to ``Flask.url_for``

        Returns
        -------
        str or None
            Generated url or None
        """

        rule = self.get_delete_url_rule()
        if rule:
            return url_for(rule, **kwargs)

        return None
