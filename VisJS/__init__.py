# Copyright (c) 2018 Pasi Lammi
# 
import json

class VisJS:
  nodes = {}
  edges = []
  template = None
  current_id = 0
  title = None

  def __init__(self,title=''):
      self.nodes = {}
      self.edges = []
      self.title = title

  def get_id(self):
    self.current_id += 1
    return self.current_id

  def json_nodes(self):
    ret = []
    for entry in self.nodes:
        r = {}
        for k,v in self.nodes[entry].iteritems():
            r[k] = v
        if r.has_key('image'):
            r["shape"] = "image"
        if r.has_key('name'):
            del r['name']
        ret.append(r)
    return json.dumps(ret, indent=2)

  def json_edges(self):
    ret = []
    for entry in self.edges:
        r = {'from': entry['src'], 'to': entry['dst']}
        ret.append(r)
    return json.dumps(ret, indent=2)

  def add_node(self,data):
    if not self.nodes.has_key(data['name']):
        name = data['name']
        self.nodes[name] = {}
        for k, v in data.iteritems():
            self.nodes[name][k] = v
        if not self.nodes[name].has_key('id'):
            self.nodes[name]['id'] = self.get_id()

  def add_edge(self,s,d):
    src = s['name']
    dst = d['name']
    if self.nodes.has_key(src) and self.nodes.has_key(dst):
        self.edges.append({'src': self.nodes[src]['id'], 'dst': self.nodes[dst]['id'] })

  def read_template(self,filename):
       with open(filename, 'r') as f:
           self.template = f.read()

  
  def print_template(self):
    n = self.json_nodes()
    e = self.json_edges()
    t = self.title
    data = { 'nodes': n, 'edges': e, 'title': t }
    print self.template % data
