#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
from os import path
from datetime import datetime
from argparse import ArgumentParser
import subprocess

post_dir = path.join(path.dirname(__file__), 'content', 'posts')

parser = ArgumentParser()
parser.add_argument('slug', type=str)
parser.add_argument('--ext', type=str, default='md')
parser.add_argument('--title', type=str, default='Title')
parser.add_argument('--category', type=str, default='')
parser.add_argument('--tags', type=str, nargs='+')
parser.add_argument('--public', default=False, action='store_const', const=True)


def make_post_file():
    options = parser.parse_args()
    time = datetime.now()
    date = '{date.year}-{date.month}-{date.day}'.format(date=time)
    fname = '{date}_{opt.slug}.{opt.ext}'.format(date=date, opt=options)

    fpath = path.join(post_dir, fname)
    if path.exists(fpath):
        ans = input('File {} already exists. Overwrite it? (y/N)'.format(fpath))
        if ans != 'y':
            print('cancelled')
            sys.exit(0)

    with open(fpath, 'w') as f:
        f.write('Title: {}\n'.format(options.title))
        f.write('Slug: {}\n'.format(options.slug))
        f.write('Date: {0} {1.hour}:{1.minute}\n'.format(date, time))
        f.write('Category: {}\n'.format(options.category))
        if options.tags:
            f.write('Tags: {}\n'.format(', '.join(options.tags)))
        else:
            f.write('Tags:\n')
        if options.public:
            f.write('Status: published\n')
        else:
            f.write('Status: draft\n')

    subprocess.run(['vim', fpath])


if __name__ == '__main__':
    make_post_file()
