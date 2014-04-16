import sys
sys.path.append('..')
from src.packet import Packet

class BroadcastPacket(Packet):
    def __init__(self, source_address, destination_address, ident, ttl, protocol, body, length, from_node, broken_links):
        super(BroadcastPacket, self).__init__(source_address=source_address, destination_address=destination_address,
                                     ident=ident, ttl=ttl, protocol=protocol, body=body, length=length)
        self.from_node = from_node
        self.broken_links = broken_links