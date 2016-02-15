#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from subprocess import run
from livereload import Server, shell

run(['make', 'html'])
server = Server()
server.watch('*.py', shell('make html'))
server.watch('content/*.md', shell('make html'))
server.watch('content/posts/*.md', shell('make html'))
server.watch('plugins/*.py', shell('make html'))
server.serve(port=8889, restart_delay=0.1, root='./output')
