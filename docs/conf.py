# -*- coding: utf-8 -*-

"""
.. module:: docs
   :synopsis: Sphinx documentation configuration
"""

import sys
import os

# Add flask_velox to the Path
root = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        '..',
    )
)

sys.path.append(os.path.join(root, 'flask_velox'))


import flask_velox  # noqa


# Project details
project = u'Flask-Velox'
copyright = u'2014, Soon London Ltd'
version = open(os.path.join(root, 'VERSION')).read()
release = open(os.path.join(root, 'VERSION')).read()

# Sphinx Config
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'

extensions = [
    'sphinx.ext.autodoc',
    'sphinxcontrib.napoleon',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.coverage',
    'sphinx.ext.ifconfig']

exclude_patterns = []

# Theme
sys.path.append(os.path.abspath('_themes'))
html_theme_path = ['_themes', ]
html_static_path = ['_static', ]
html_theme = 'kr'
html_sidebars = {
    'index':    ['sidebar_intro.html', 'localtoc.html', 'relations.html',
                 'sourcelink.html', 'searchbox.html'],
    '**':       ['sidebar_intro.html', 'localtoc.html', 'relations.html',
                 'sourcelink.html', 'searchbox.html']
}
