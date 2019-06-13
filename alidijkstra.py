from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.recoco import Timer
from collections import defaultdict
from pox.openflow.discovery import Discovery
from pox.lib.util import dpid_to_str
import time
import copy

log = core.getLogger()
mac_map = {}
switches = {}
myswitches = []
adjacency = defaultdict(lambda: defaultdict(lambda: None))
current_p = []

def minimum_distance(distance, Q):
    #print "distance=", distance
    #print "Q=", Q

    min = float('Inf')
    node = 0

    for v in Q:
        if distance[v] < min:
		min = distance[v]
        	node = v

    #print "min=", min, " node=", node
    return node


def _get_raw_path(src, dst):
    # Dijkstra algorithm

    print
    "src=", src, " dst=", dst

    # print "myswitches=", myswitches
    distance = {}
    previous = {}
    sws = myswitches

    for dpid in sws:
        distance[dpid] = float('Inf')
        previous[dpid] = None

    distance[src] = 0
    Q = set(sws)

    while len(Q) > 0:
        u = minimum_distance(distance, Q)
        # print "u=", u
        Q.remove(u)

        for p in sws:
            if adjacency[u][p] != None:
                w = 1

                if distance[u] + w < distance[p]:
                    distance[p] = distance[u] + w
                    previous[p] = u
    r = []
    p = dst
    r.append(p)
    q = previous[p]

    while q is not None:

        if q == src:
            r.append(q)
            break
        p = q
        r.append(p)
        q = previous[p]
    r.reverse()
    return r

class Switch (EventMixin):
    def __init__ (self):
        self.connection = None
        self.ports = None
        self.dpid = None
        self._listeners = None
        self._connected_at = None
        mac_map[str("00:00:00:00:00:01")]=(1,1)
        mac_map[str("00:00:00:00:00:02")]=(36,1)

    def __repr__(self):
        return dpid_to_str(self.dpid)

    def _install(self, in_port, out_port, match, buf=None):
        msg = of.ofp_flow_mod()
        msg.match = match
        msg.match.in_port = in_port
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.actions.append(of.ofp_action_output(port=out_port))
        msg.buffer_id = buf
        self.connection.send(msg)

    def _handle_PacketIn(self, event):
        global current_p

        print
        "_hanle_PacketIn() is called at", self.dpid

        packet = event.parsed
        print
        "packet.src=", str(packet.src), " packet.dst=", packet.dst

        if str(packet.src) != "00:00:00:00:00:01" and str(packet.src) != "00:00:00:00:00:02":
            return
            # print "switches=", switches

        # print "adjacency=", adjacency
        path = _get_raw_path(mac_map[str(packet.src)][0], mac_map[str(packet.dst)][0])
        # if len(current_p)!=0 and current_p != path:
        #  del current_p[:]

        current_p = copy.deepcopy(path)
        print
        "path=", path, "current_p=", current_p

        if mac_map[str(packet.dst)][0] != self.dpid:
            next = path[path.index(self.dpid) + 1]

            # print "next=", next
            output_port = adjacency[self.dpid][next]
            # print "output_port=", adjacency[self.dpid][next]
            match = of.ofp_match.from_packet(packet)
            self._install(event.port, output_port, match)

        else:
            output_port = mac_map[str(packet.dst)][1]

        msg = of.ofp_packet_out()
        msg.actions.append(of.ofp_action_output(port=output_port))
        msg.buffer_id = event.ofp.buffer_id
        msg.in_port = event.port
        self.connection.send(msg)

    def disconnect(self):
        if self.connection is not None:
            log.debug("Disconnect %s" % (self.connection,))
            self.connection.removeListeners(self._listeners)
            self.connection = None
            self._listeners = None

    def connect(self, connection):
        # print "type(conection.dpid)=", type(connection.dpid)
        if self.dpid is None:
            self.dpid = connection.dpid

        assert self.dpid == connection.dpid

        if self.ports is None:
            self.ports = connection.features.ports

        self.disconnect()
        log.debug("Connect %s" % (connection,))
        self.connection = connection
        self._listeners = self.listenTo(connection)
        self._connected_at = time.time()

    def _handle_ConnectionDown(self, event):
        self.disconnect()


class l2_multi(EventMixin):
    def __init__(self):
        # Listen to dependencies

        def startup():
            core.openflow.addListeners(self, priority=0)
            core.openflow_discovery.addListeners(self)
        core.call_when_ready(startup, ('openflow', 'openflow_discovery'))

    def _handle_ConnectionUp(self, event):
        sw = switches.get(event.dpid)

        if sw is None:
            # New switch
            sw = Switch()
            switches[event.dpid] = sw
            sw.connect(event.connection)
            myswitches.append(event.dpid)

        else:
            sw.connect(event.connection)

    def _handle_LinkEvent(self, event):
        global current_p
        l = event.link
        sw1 = l.dpid1
        sw2 = l.dpid2
        pt1 = l.port1
        pt2 = l.port2
        no_edges = 0

        for p in myswitches:
            for q in myswitches:
                if adjacency[p][q] != None:
                    no_edges += 1

        print
        "number of edges=", (no_edges * 0.5)

        print
        "current_p=", current_p

        if len(myswitches) == 37 and (no_edges * 0.5) == 56:
            if event.removed:
                print
                sw1, "----", sw2, " is removed"

            clear = of.ofp_flow_mod(command=of.OFPFC_DELETE)
            for dpid in current_p:
                if switches[dpid].connection is None: continue
                switches[dpid].connection.send(clear)

        if event.added:
            # print "link is added"

            if adjacency[sw1][sw2] is None:
                adjacency[sw1][sw2] = l.port1
                adjacency[sw2][sw1] = l.port2

        if event.removed:
            # print "link is removed"
            try:
                if sw2 in adjacency[sw1]: del adjacency[sw1][sw2]
                if sw1 in adjacency[sw2]: del adjacency[sw2][sw1]

            except:

                print
                "remove edge error"

def launch ():
  core.registerNew(l2_multi)
