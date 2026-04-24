from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.packet.arp import arp
from pox.lib.packet.ethernet import ethernet

log = core.getLogger()

class ArpController (object):
    def __init__ (self):
        core.openflow.addListeners(self)
        self.mac_to_port = {} # Learning table

    def _handle_PacketIn (self, event):
        packet = event.parsed
        in_port = event.port

        # Learn source MAC
        self.mac_to_port[packet.src] = in_port

        # Handle ARP Packets
        if packet.type == ethernet.ARP_TYPE:
            arp_pkt = packet.find('arp')
            log.info("ARP intercepted: %s is looking for %s", arp_pkt.hwsrc, arp_pkt.protodst)
            
            # Flood the ARP request so it finds the host
            msg = of.ofp_packet_out()
            msg.data = event.ofp
            msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
            event.connection.send(msg)
            return

        # Handle IP Packets (Ping) and install Flow Rules
        if packet.dst in self.mac_to_port:
            out_port = self.mac_to_port[packet.dst]
            
            # Install Flow Rule: Match destination MAC -> Output to Port
            msg = of.ofp_flow_mod()
            msg.match = of.ofp_match.from_packet(packet)
            msg.actions.append(of.ofp_action_output(port = out_port))
            event.connection.send(msg)
            
            # Also send the current packet out
            msg_out = of.ofp_packet_out()
            msg_out.data = event.ofp
            msg_out.actions.append(of.ofp_action_output(port = out_port))
            event.connection.send(msg_out)
            log.info("Flow Rule Installed for %s on port %d", packet.dst, out_port)

def launch ():
    core.registerNew(ArpController)
