#!/usr/bin/env python 

# Copyright (c) 2018 Pasi Lammi
#

# read routes from proc filesystem and print them out to html
# usage: python example_linux_route.py > data.html

from VisJS import VisJS
import os
import json
import socket

template_filename = '%s/vis.html' % (os.path.dirname(os.path.realpath('__file__')))
vis = VisJS('kernel routes')
vis.read_template(template_filename)


def to_ip_formatted(s):
  return '.'.join(str(int(i, 16)) for i in reversed([s[i:i+2] for i in range(0, len(s), 2)]))

routes=[]
with open('/proc/net/route') as f:
  for line in f:
    d = line.rstrip().split("\t")
    if not len(d) == 11:
      continue
    interface = d[0]
    network = to_ip_formatted(d[1])
    netmask = to_ip_formatted(d[7])
    gateway = to_ip_formatted(d[2])
    routes.append({ 'network': network, 'netmask': netmask, 'gateway': gateway })

me = socket.gethostname()
hostnode = { 'name': "host-%s" % (me), 'label': me }
vis.add_node(hostnode)

for route in routes:
    node = { 'name': "gw-%s" % (route['gateway']), 'label': route['gateway'] }
    vis.add_node(node)
    vis.add_edge(hostnode,node)

    name = "network-%sm%s" % (route['network'], route['netmask'])
    label = "%sm%s" % (route['network'], route['netmask'])
    node2 = { 'name': name, 'label': label }
    vis.add_node(node2)
    vis.add_edge(node,node2)
    

vis.print_template()
