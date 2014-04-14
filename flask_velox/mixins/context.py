# -*- coding: utf-8 -*-

"""
Module provides mixin classes for dealing with updating context passed to
templates for rendering.

Example
-------

>>> from flask.ext.velox.mixins.context import ContextMixin
... from flask.ext.velox.mixins.template import TemplateMixin
...
... app = Flask(__name__)
...
... class MyView(TemplateMixin, ContextMixin):
...     default_context = {
...         'foo': 'bar'
...     }
...
... app.add_url_rule('/', view_func=MyView.as_view('myview'))
...
... app.run()

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
    >>> class FooView(ContextMixin):
    ...     default_context = {
    ...         'foo': 'bar',
    ...     }

    """

    def __init__(self, *args, **kwargs):
        """ Constructor

        Performs initial setup defining `_context` and merging
        `default_context`.
        """

        #: Holds the context value for the instance
        self._context = {}

        default_context = getattr(self, 'default_context', {})
        self.merge(default_context)

    @property
    def context(self):
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
        ...     default_context = {
        ...         'foo': 'bar',
        ...     }
        ...
        >>> view = FooView()
        >>> view.update_context({'hello': 'world'})
        True
        >>> view.context
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
        ...     default_context = {
        ...         'foo': 'bar',
        ...     }
        ...
        >>> view = FooView()
        >>> view.merge_context({'hello': 'world'})
        >>> view.context
        {
            'hello': 'world',
            'foo': 'bar'
        }

        Returns
        -------
        dict
            The new context

        """

        _context = self._context
        new = dict(_context.items() + subject.items())
        self._context = new

        return new

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
        bool
            Success or Failure
        """

        context = self.context
        context[key] = val

        return True

    def del_context(self, key):
        """
        Removes an element from the context dictionary.

        Example
        -------
        >>> class FooView(ContextMixin):
        ...     default_context = {
        ...         'foo': 'bar',
        ...     }
        ...
        >>> view = FooView()
        >>> view.del_context('foo')
        True
        >>> view.context
        {}

        Arguments
        ---------
        key : str
            The context key name

        Returns
        -------
        bool
            Success or Failure
        """

        context = self.context

        try:
            context.pop(key, None)
            self._context = context
        except KeyError:
            return False

        return True
