#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'miyakogi'
SITENAME = 'Blank File'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Asia/Tokyo'

DEFAULT_LANG = 'ja'

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
THEME = 'theme/pelican-bootstrap3'
BOOTSTRAP_THEME = ''
PYGMENTS_STYLE = 'trac'

# Social
# GITHUB_USER = ''
# GITHUB_REPO_COUNT = 3
# GITHUB_SKIP_FORK = True
TWITTER_USERNAME = 'miyakodev'
TWITTER_WIDGET_ID = '695483665627766784'
ADDTHIS_PROFILE = 'ra-56b43892ef18a159'

# Plugins
PLUGIN_PATHS = ['plugins']
PLUGINS = ['tag_cloud']

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
