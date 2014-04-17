# -*- coding: utf-8 -*-

""" Methods tp be used when formatting field outputs, for example in tables.
"""

import pytz

from jinja2 import Markup


def bool_formatter(value, true='Yes', false='No'):
    """ For rendering True / False values in a human friendly way, by default
    True = Yes and False = No however this can be overriden by passing
    true and false keyword args with their respective values.

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

    Arguments
    ---------
    value : bool
        The value to evaluate against

    Returns
    -------
    str
        Formatted date time
    """

    value = value.replace(tzinfo=pytz.utc)
    return value.strftime('%d/%m/%Y at %I:%M%p %Z')
