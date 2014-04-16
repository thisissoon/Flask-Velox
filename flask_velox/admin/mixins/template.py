# -*- coding: utf-8 -*-

"""
Module provides mixin classes for integrating ``Flask-Velox`` Views with
``Flask-Admin``.
"""

from flask_velox.mixins.template import TemplateMixin


class AdminTemplateMixin(TemplateMixin):
    """ Overrides default ``TemplateMixin`` methods to provide admin
    rendering functionality.

    Note
    ----
    * Flask-Admin must be installed
    * Overrides :py:class:`flask_velox.mixins.template.TemplateMixin`

    """

    def get_admin(self):
        """ Returns the current admin system to render templates within the
        ``Flask-Admin`` system.

        Returns
        -------
        obj
            Current admin view

        """

        try:
            return self._admin
        except AttributeError:
            raise NotImplementedError('``_admin`` has not been declared.')

    def render(self):
        """ Renders template within the ``Flask-Admin`` system.

        Note
        ----
        Overrides: :py:meth:`flask_velox.mixins.template.TemplateMixin.render`

        """

        admin = self.get_admin()

        return admin.render(
            self._template,
            **getattr(self, 'context', {}))

    def get(self, admin, *args, **kwargs):
        """ Handles HTTP GET requests to View. Also sets ``self._admin``
        which contains the passed admin view.

        Arguments
        ---------
        admin : obj
            The current admin view

        Note
        ----
        Overrides: :py:meth:`flask_velox.mixins.template.TemplateMixin.get`

        """

        self._admin = admin
        return super(AdminTemplateMixin, self).get(*args, **kwargs)
