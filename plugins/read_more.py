#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pelican import signals
from pelican.utils import truncate_html_words


def truncate(generator):
    read_more_tag = generator.settings.get('READ_MORE_TAG', '<!-- more -->')
    max_length = generator.settings.get('SUMMARY_MAX_LENGTH')
    for article in generator.articles:
        content = article.content
        if read_more_tag in content:
            article._summary = content[0:content.find(read_more_tag)]
        else:
            article._summary = truncate_html_words(content, max_length)


def register():
    signals.article_generator_finalized.connect(truncate)
    # signals.all_generators_finalized.connect(truncate_all)
