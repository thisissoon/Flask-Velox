# -*- coding: utf-8 -*-

""" Module provides mixins for issuing HTTP Status codes using the
Flask ``View``.
"""

from flask import url_for
from flask.views import View
from werkzeug.utils import redirect


class RedirectMixin(View):
    """ Raise a HTTP Redirect, by default a 302 HTTP Status Code will be used
    however this can be overridden using the ``code`` attribute.

    Example
    -------

    .. code-block:: python
        :linenos:

        from flask.ext.velox.mixins.http import RedirectMixin
        class MyView(RedirectMixin):
            rule = 'some.url.rule'
            code = 301

    Attributes
    ----------
    rule : str
        Flask URL Rule passed into ``url_for``
    code : int, optional
        Status code to raise, defaults to ``302``
    """

    code = 302

    def pre_dispatch(self, *args, **kwargs):
        """ If you wish to run an arbitrary piece of code before the
        redirect is dispatched you can override this method which is
        called before dispatch.
        """

        pass

    def get_url(self):
        """ Return a generated url from ``rule`` attribute.

        Returns
        -------
        str
            Generated url
        """

        try:
            rule = self.rule
        except AttributeError:
            raise NotImplementedError('``rule`` attr must be defined.')

        return url_for(rule)

    def dispatch_request(self, *args, **kwargs):
        """ Dispatch the request, returning the redirect.func_closure

        Returns
        -------
        werkzeug.wrappers.Response
            Redirect response
        """

        self.pre_dispatch()
        return redirect(self.get_url(), code=getattr(self, 'code', 302))
