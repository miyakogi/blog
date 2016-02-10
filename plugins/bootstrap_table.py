#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

from pelican import signals

add_table_re = re.compile(r'<table>')

def add_table_class(gen):
    for article in gen.articles:
        if '<table>' in article._content:
            article._content = add_table_re.sub(r'<table class="table">', article._content)

def register():
    signals.article_generator_finalized.connect(add_table_class)
