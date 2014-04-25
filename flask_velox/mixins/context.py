# -*- coding: utf-8 -*-

"""
Module provides mixin classes for dealing with updating context passed to
templates for rendering.

Example
-------

.. code-block:: python
    :linenos:

    from flask.ext.velox.mixins.context import ContextMixin
    from flask.ext.velox.mixins.template import TemplateMixin

    app = Flask(__name__)

    class MyView(TemplateMixin, ContextMixin):
        context = {
            'foo': 'bar'
        }

    app.add_url_rule('/', view_func=MyView.as_view('myview'))

    app.run()

"""


class ContextMixin(object):
    """ Mixin this class to add context support to template
    rendering. Default context can be defined by setting the ``context``
    attribute to contain a ``dict`` of key value pairs.

    Attributes
    ----------
    context : dict, optional
        Default context to use when rendering the template

    Example
    -------

    .. code-block:: python
        :linenos:

        class FooView(ContextMixin):
            context = {
                'foo': 'bar',
            }

    """

    def __init__(self, *args, **kwargs):
        """ Constructor

        Performs initial setup defining `_context` and merging
        `context`.
        """

        #: Holds the context value for the instance
        self._context = {}

        # Merge default context into context if exists
        context = getattr(self, 'context', {})
        self.merge_context(context)

        # Call a callback method so class extending this can
        # have a method override just for context rather than
        # overridding HTTP verb methods such as get, post etc
        if hasattr(self, 'set_context'):
            self.merge_context(self.set_context())

        super(ContextMixin, self).__init__(*args, **kwargs)

    def get_context(self):
        """ Propety method which returns the current context.

        Returns
        -------
        dict
           Current context value

        """

        _context = getattr(self, '_context', {})

        if not hasattr(self, '_context'):
            self._context = _context

        return _context

    def update_context(self, new):
        """ Overwrites the existing context with the provided new context
        value.

        Example
        -------
        >>> class FooView(ContextMixin):
        ...     context = {
        ...         'foo': 'bar',
        ...     }
        ...
        >>> view = FooView()
        >>> view.update_context({'hello': 'world'})
        {
            'hello': 'world'
        }

        Arguments
        ---------
        new : dict
            Value to update context too

        Returns
        -------
        dict
            The new context
        """

        self._context = new

        return new

    def merge_context(self, subject):
        """ Merge the passed dictionary into the current `_context`

        Arguments
        ---------
        subject : dict
            The `dict` to merge into `_context`

        Example
        -------
        >>> class FooView(ContextMixin):
        ...     context = {
        ...         'foo': 'bar',
        ...     }
        ...
        >>> view = FooView()
        >>> view.merge_context({'hello': 'world'})
        >>> view.get_context()
        {
            'hello': 'world',
            'foo': 'bar'
        }

        Returns
        -------
        dict
            The new context

        """

        context = self.get_context()

        if subject:
            context = dict(context.items() + subject.items())
            self._context = context

        return context

    def set_context(self):
        """ A method which should be overridden when required to set extra
        context on a per view basis. This method is not required to be
        implemented however is the recommended way of setting extra context
        """

        pass

    def add_context(self, key, val):
        """
        Adds a new element to the context.

        Arguments
        ---------
        key : str
            The context key name
        val
            The value of the new context item of any type

        Returns
        -------
        dict
            The new context
        """

        context = self.get_context()
        context[key] = val

        self._context = context

        return context

    def del_context(self, key):
        """
        Removes an element from the context dictionary.

        Example
        -------
        >>> class FooView(ContextMixin):
        ...     context = {
        ...         'foo': 'bar',
        ...     }
        ...
        >>> view = FooView()
        >>> view.del_context('foo')
        {}

        Arguments
        ---------
        key : str
            The context key name

        Returns
        -------
        bool
            Success or Failure

        Returns
        -------
        dict
            The new context
        """

        context = self.get_context()

        try:
            context.pop(key, None)
            self._context = context
        except KeyError:
            return False

        return context
