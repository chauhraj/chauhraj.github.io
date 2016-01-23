#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
from getpass import getuser
import os


AUTHOR = u'Rajiv Chauhan'
SITENAME = u'Notes to myself...'
SITEURL = ''

HOME = os.getenv('HOME')

PATH = 'content'
PLUGIN_PATHS = [os.path.join(HOME, ".pelican", "pelican-plugins")]

TIMEZONE = 'America/New_York'
#THEME = 'personal'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('twitter', 'http://twitter.com/chauhraj'),
          ('github', 'http://github.com/chauhraj'),)

DEFAULT_PAGINATION = 10
DEFAULT_DATE = 'fs'

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

STATIC_PATHS = ['images', 'extra/CNAME']
PLUGINS = ['assets', 'render_math']
