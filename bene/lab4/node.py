import sys
sys.path.append('..')
from src.node import Node

class Node(Node):
    def __init__(self, hostname):
        super(Node, self).__init__(hostname)
        self.hostname = hostname
        self.distanceVector = {}

    def add_node_to_vector(self, address, distance, link):
        self.distanceVector[address] = [distance, link, []]