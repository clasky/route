import sys
import os
from node import Node
from BroadcastPacket import BroadcastPacket
sys.path.append('..')
from src.sim import Sim
from src import link
from src.packet import Packet
from networks.network import Network

NETWORK_FILE_PATH = "../networks/five-node-ring.txt"

class Broadcast(object):
    def __init__(self, duration, node):
        self.duration = duration
        self.rootNode = node
        self.start = 0

    # noinspection PyDocstring
    def sendBroadcast(self,event):
        # quit if done
        now = Sim.scheduler.current_time()
        if (now - self.start) > self.duration:
            return

        Sim.trace("Broadcasting...")
        bp = BroadcastPacket(source_address=0, destination_address=0, ident=2, ttl=1, protocol='broadcast',
                            body=self.rootNode.distanceVector, length=0, from_node=self.rootNode, broken_links=set())
        Sim.scheduler.add(delay=0, event=bp, handler=self.rootNode.send_packet)

        # schedule the next time we should generate a packet
        Sim.scheduler.add(delay=1, event='broadcast', handler=self.sendBroadcast)

# noinspection PyDocstring
class BroadcastApp(object):
    def __init__(self, node):
        self.node = node
        self.broken_links = set()
        
    def receive_packet(self, packet):
        rebroadcast = False
        link = self.findLink(packet)

        # Always check for boken links
        for b_link in self.node.links:
            if not b_link.running:
                self.broken_links.add(b_link.address)
            else:
                if b_link in self.broken_links:
                    self.broken_links.remove(b_link)


        # If the two sets are not equal then remove links from distance vectors else they are up to date
        if len(self.broken_links - packet.broken_links) != 0 or len(packet.broken_links - self.broken_links) != 0:
            self.broken_links = self.broken_links.union(packet.broken_links)

            addressToRemove = set()
            for address in self.node.distanceVector:
                for a_link in self.broken_links:
                    if a_link in self.node.distanceVector:
                        addressToRemove.add(a_link)
                    for b_link in self.node.distanceVector[address][2]:
                        if b_link.address == a_link:
                            addressToRemove.add(address)

            for address in addressToRemove:
                del self.node.distanceVector[address]
            rebroadcast = True
        else:
            for address in packet.body:
                if not address in self.node.distanceVector:
                    self.node.add_node_to_vector(address, -1, link)
                    self.node.distanceVector[address][2].append(link)

                if(self.node.distanceVector[address][0] > packet.body[address][0]) \
                        or (self.node.distanceVector[address][0] == -1 and packet.body[address][0] != -1):
                    if self.node.distanceVector[address][0] != packet.body[address][0] + 1:
                        self.node.distanceVector[address][0] = packet.body[address][0] + 1
                        self.node.distanceVector[address][2].extend(packet.body[address][2])
                        self.node.delete_forwarding_entry(address, link)
                        self.node.add_forwarding_entry(address, link)
                        rebroadcast = True

        if rebroadcast:
            self.broadcast(self.node, link)

    def findLink(self, packet):
        for link in self.node.links:
            if link.endpoint.hostname == packet.from_node.hostname:
                return link

    def broadcast(self, node, link):
        bp = BroadcastPacket(source_address=link.address, destination_address=0, ident=2, ttl=1, protocol='broadcast',
                            body=node.distanceVector, length=0, from_node=node, broken_links=self.broken_links)
        Sim.scheduler.add(delay=0, event=bp, handler=node.send_packet)


if __name__ == '__main__':
    # parameters
    Sim.scheduler.reset()
    Sim.set_debug(False)

    network = Network(os.path.abspath(NETWORK_FILE_PATH))

    for key in network.nodes:
        b = BroadcastApp(network.nodes[key])
        network.nodes[key].add_protocol(protocol="broadcast", handler=b)

    # start initial broadcast
    broadcast = Broadcast(10, network.get_node('n1'))
    Sim.scheduler.add(delay=0, event='broadcast', handler=broadcast.sendBroadcast)

    # send one packet
    p = Packet(destination_address=8, ident=1, protocol='delay', length=1000)
    Sim.scheduler.add(delay=1, event=p, handler=network.get_node('n2').send_packet)

    # drop a link
    Sim.scheduler.add(delay=2, event=None, handler=network.get_node('n3').links[0].down)
    Sim.scheduler.add(delay=2, event=None, handler=network.get_node('n2').links[1].down)

    # resend same packet
    p = Packet(destination_address=8, ident=1, protocol='delay', length=1000)
    Sim.scheduler.add(delay=3, event=p, handler=network.get_node('n2').send_packet)

    # bring back link
    Sim.scheduler.add(delay=4, event=None, handler=network.get_node('n3').links[0].up)
    Sim.scheduler.add(delay=4, event=None, handler=network.get_node('n2').links[1].up)

    # resend same packet
    p = Packet(destination_address=8, ident=1, protocol='delay', length=1000)
    Sim.scheduler.add(delay=5, event=p, handler=network.get_node('n2').send_packet)

    # run the simulation
    Sim.scheduler.run()