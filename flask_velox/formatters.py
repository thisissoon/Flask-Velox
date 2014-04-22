# -*- coding: utf-8 -*-

""" Helper functions to assist in formatting data when rendering object data.
"""

import pytz

from jinja2 import Markup


def bool_formatter(value, true='Yes', false='No'):
    """ For rendering True / False values in a human friendly way, by default
    True = Yes and False = No however this can be overriden by passing
    true and false keyword args with their respective values.

    Example
    -------

    >>> from flask.ext.velox.formatters import bool_formatter
    >>> bool_formatter(True)
    'Yes'
    >>> bool_formatter(False)
    'No'

    Arguments
    ---------
    value : bool
        The value to evaluate against
    true : str, optional
        Value to use for True state, defaults to 'Yes'
    false : str, optional
        Value to use for False state, defaults to 'No'

    Returns
    -------
    str
        The value to use
    """

    if value is True:
        return true
    else:
        return false


def bool_admin_formatter(value):
    """ Render booleans using HTML rather than plain text for the
    ``Flask-Admin`` system using bootstrap markup.

    Example
    -------

    >>> from flask.ext.velox.formatters import bool_admin_formatter
    >>> bool_admin_formatter(True)
    '<i class="icon-ok"></i>'
    >>> bool_admin_formatter(False)
    '<i class="icon-remove"></i>'

    Arguments
    ---------
    value : bool
        The value to evaluate against

    Returns
    -------
    str
        The html value to use
    """

    return Markup(bool_formatter(
        value,
        true='<i class="icon-ok"></i>',
        false='<i class="icon-remove"></i>'))


def datetime_formatter(value):
    """ Render a sane date time value, for example: dd/mm/yyyy at HH:MM TZ.
    All values should be UTC.

    Example
    -------

    >>> import datetime
    >>> from flask.ext.velox.formatters import datetime_formatter
    >>> now = datetime.datetime.utcnow()
    >>> datetime_formatter(now)
    '11/04/2014 at 10:49AM UTC'

    Arguments
    ---------
    value : datetime
        Datetime object to format

    Returns
    -------
    str
        Formatted date time
    """

    value = value.replace(tzinfo=pytz.utc)
    return value.strftime('%d/%m/%Y at %I:%M%p %Z')
