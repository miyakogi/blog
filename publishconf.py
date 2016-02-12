#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

SITEURL = 'https://miyakogi.github.io/blog'
RELATIVE_URLS = False

FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/%s.atom.xml'

# Social
# GITHUB_USER = ''
# GITHUB_REPO_COUNT = 3
# GITHUB_SKIP_FORK = True
TWITTER_USERNAME = 'miyakodev'
TWITTER_WIDGET_ID = '695483665627766784'
ADDTHIS_PROFILE = 'ra-56b43892ef18a159'


DELETE_OUTPUT_DIRECTORY = True

# Following items are often useful when publishing

#DISQUS_SITENAME = ""
GOOGLE_ANALYTICS = 'UA-59101475-2'
