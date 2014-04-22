# -*- coding: utf-8 -*-

""" Module provides views for issuing HTTP status codes using
Flask ``MethodView``.
"""

from flask_velox.mixins.http import RedirectMixin


class RedirectView(RedirectMixin):
    """ View for raising a HTTP 3XX Response. By default this View
    will raise a HTTP 302 however this can be overridden by defining a
    ``code`` attribute.

    Example
    -------

    .. code-block:: python
        :linenos:

        from flask.ext.velox.views.http import RedirectView
        class MyView(RedirectMixin):
            rule = 'some.url.rule'
            code = 301

    See Also
    --------
    * :py:class:`flask_velox.mixins.http.RedirectMixin`
    """

    pass
