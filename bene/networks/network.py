import sys
sys.path.append('..')

from src import link
from src import node
from node import Node

class Network(object):
    def __init__(self,config):
        self.config = config
        self.nodes = {}
        self.address = 1
        self.build()

    def build(self):
        with open(self.config) as f:
            for line in f.readlines():
                if line.startswith('#'):
                    continue
                fields = line.split()
                if len(fields) < 2:
                    continue
                start = self.get_node(fields[0])
                for i in range(1,len(fields)):
                    end = self.get_node(fields[i])
                    #print(fields[0] + " " + str(self.address) + " " + fields[i])
                    l = link.Link(self.address,start,endpoint=end)
                    start.add_node_to_vector(self.address, 0, l)
                    self.address += 1
                    start.add_link(l)
                
    def get_node(self,name):
        if name not in self.nodes:
            self.nodes[name] = Node(name)
        return self.nodes[name]
