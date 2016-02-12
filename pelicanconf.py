#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'miyakogi'
SITENAME = 'Blank File'
SITEURL = ''

PATH = 'content'
# STATIC_PATHS = ['images']

TIMEZONE = 'Asia/Tokyo'

DEFAULT_LANG = 'ja'

ARTICLE_URL = 'posts_{date:%Y}-{date:%m}-{date:%d}_{slug}.html'
ARTICLE_SAVE_AS = 'posts_{date:%Y}-{date:%m}-{date:%d}_{slug}.html'

# Menu
DISPLAY_CATEGORIES_ON_MENU = False

# Summary
SUMMARY_MAX_LENGTH = 20

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (
    ('Python.org', 'http://python.org/'),
    ('Pelican', 'http://getpelican.com/'),
)

# Social widget
SOCIAL = (('github', 'https://github.com/miyakogi'),
          ('twitter', 'https://twitter.com/MiyakoDev'),)

DEFAULT_PAGINATION = 10

# Sidebar

DISPLAY_TAGS_ON_SIDEBAR = True
DISPLAY_CATEGORIES_ON_SIDEBAR = True
DISPLAY_RECENT_POSTS_ON_SIDEBAR = True

# Theme
THEME = 'theme/mybs'
# http://getbootstrap.com/customize/?id=910fb5350e7add900d1d
BOOTSTRAP_THEME = 'ja'
BOOTSTRAP_NAVBAR_INVERSE = False
PYGMENTS_STYLE = 'trac'

# Plugins
PLUGIN_PATHS = ['plugins']
PLUGINS = ['tag_cloud', 'bootstrap_table', 'read_more']

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
