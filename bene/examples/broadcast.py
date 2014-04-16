import sys
from node import Node

sys.path.append('..')

from src.sim import Sim
from src import link
from src import packet

import random

class DistanceVector(object):
    def __init__(self,address,distance,node,link):
        self.vector = {address : [distance,node,link]}
        
class BroadcastApp(object):
    def __init__(self,node):
        self.node = node

    def receive_packet(self,packet):
        print Sim.scheduler.current_time(),self.node.hostname,packet.ident
    
def broadcast(nodeHandlers):
	for i in nodeHandlers:	
		for j in range (0,5):
			sourceAddress = j + 1
			p = packet.Packet(source_address=sourceAddress,destination_address=0,ident=2,ttl=1,protocol='broadcast',length=100)
			Sim.scheduler.add(delay=0, event=p, handler=nodeHandlers[j].send_packet)
 
if __name__ == '__main__':
    # parameters
    Sim.scheduler.reset()
    Sim.set_debug(True)

    # setup network
    n1 = Node('n1')
    n2 = Node('n2')
    n3 = Node('n3')
    n4 = Node('n4')
    n5 = Node('n5')
    
    nodeHandlers = [n1,n2,n3,n4,n5]
    
    # link from 1 to 2
    l = link.Link(address=1,startpoint=n1,endpoint=n2)
    dv1 = DistanceVector(1,0,n1,l)
    n1.add_link(l)
    # link from 2 to 1
    l = link.Link(address=2,startpoint=n2,endpoint=n1)
    dv2 = DistanceVector(2,0,n2,l)
    n2.add_link(l)
    # link from 2 to 3
    l = link.Link(address=3,startpoint=n2,endpoint=n3)
    dv3 = DistanceVector(3,0,n2,l)
    n2.add_link(l)
    # link from 3 to 2
    l = link.Link(address=4,startpoint=n3,endpoint=n2)
    dv4 = DistanceVector(4,0,n3,l)    
    n3.add_link(l)
    # link from 3 to 4
    l = link.Link(address=5,startpoint=n3,endpoint=n4)
    dv5 = DistanceVector(5,0,n3,l)
    n3.add_link(l)
    # link from 4 to 3
    l = link.Link(address=6,startpoint=n4,endpoint=n3)
    dv6 = DistanceVector(6,0,n4,l)
    n4.add_link(l)
    # link from 4 to 5
    l = link.Link(address=7,startpoint=n4,endpoint=n5)
    dv7 = DistanceVector(7,0,n4,l)    
    n4.add_link(l)
    # link from 5 to 4
    l = link.Link(address=8,startpoint=n5,endpoint=n4)
    dv8 = DistanceVector(8,0,n5,l)    
    n5.add_link(l)

    # setup broadcast application
   
    b1 = BroadcastApp(n1)
    n1.add_protocol(protocol="broadcast",handler=b1)
    b2 = BroadcastApp(n2)
    n2.add_protocol(protocol="broadcast",handler=b2)
    b3 = BroadcastApp(n3)
    n3.add_protocol(protocol="broadcast",handler=b3)
    b4 = BroadcastApp(n4)
    n4.add_protocol(protocol="broadcast",handler=b4)
    b5 = BroadcastApp(n5)
    n5.add_protocol(protocol="broadcast",handler=b5)
    
    broadcast(nodeHandlers)
    
    # run the simulation
    Sim.scheduler.run()
