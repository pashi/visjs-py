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
        for k in self.nodes[entry]:
            r[k] = self.nodes[entry][k]
        if 'image' in r:
            r["shape"] = "image"
        if 'name' in r:
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
    if not data['name'] in self.nodes:
        name = data['name']
        self.nodes[name] = {}
        #for k, v in data.iteritems():
        for k in data:
            self.nodes[name][k] = data[k]
        if not 'id' in self.nodes[name]:
            self.nodes[name]['id'] = self.get_id()

  def add_edge(self,s,d):
    src = s['name']
    dst = d['name']
    if src in self.nodes and dst in self.nodes:
        self.edges.append({'src': self.nodes[src]['id'], 'dst': self.nodes[dst]['id'] })

  def read_template(self,filename):
       with open(filename, 'r') as f:
           self.template = f.read()

  
  def print_template(self):
    n = self.json_nodes()
    e = self.json_edges()
    t = self.title
    data = { 'nodes': n, 'edges': e, 'title': t }
    print (self.template % data)
