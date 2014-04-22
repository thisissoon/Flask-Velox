# -*- coding: utf-8 -*-

""" Initialise Flask Extenstion
"""

from flask import Blueprint


class Velox(object):

    def init_app(self, app):
        """ Initialises Flask extenstion registering a Velox blueprint
        with the application context pass in.

        Arguments
        ---------
        app : object
            Flask application object
        """

        velox = Blueprint(
            'velox',
            __name__,
            template_folder='templates')

        app.register_blueprint(velox)
