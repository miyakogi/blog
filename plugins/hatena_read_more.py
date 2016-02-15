#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

from pelican import signals
from pelican.utils import truncate_html_words
from pelican.generators import ArticlesGenerator



def truncate(generator):
    read_more = generator.settings.get('READ_MORE_RE',
                                           r'<!--\s*?more\s*?-->')
    read_more_re = re.compile(r'^(.*?)' + read_more, re.S)
    max_length = generator.settings.get('SUMMARY_MAX_LENGTH')
    for article in tuple(generator.articles):
        content = article.content
        match = read_more_re.search(content)
        if match:
            article._summary = match.group(1)
        else:
            article._summary = truncate_html_words(content, max_length)


def truncate_all(generators):
    for gen in generators:
        if isinstance(gen, ArticlesGenerator):
            truncate(gen)


def register():
    signals.all_generators_finalized.connect(truncate_all)
