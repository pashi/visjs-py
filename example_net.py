#!/usr/bin/env python 

# Copyright (c) 2018 Pasi Lammi
#

# read routes from proc filesystem and print them out to html
# usage: python example_net.py > data.html

from VisJS import VisJS
import os
import json

template_filename = '%s/vis.html' % (os.path.dirname(os.path.realpath('__file__')))
vis = VisJS('network diagram')
vis.read_template(template_filename)


nodes=[]
edges=[]
data = None
with open('example_net.json') as f:
    data = json.load(f)
    for n in data['nodes']:
        vis.add_node(n)

    for n in data['edges']:
        s = { 'name': n['src'] }
        d = { 'name': n['dst'] }
        vis.add_edge(s,d)

vis.print_template()
