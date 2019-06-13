# Created By Ali Malik

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.recoco import Timer
from collections import defaultdict
from pox.openflow.discovery import Discovery
from pox.lib.util import dpid_to_str
import time
from matplotlib import pylab
import jgraph

import numpy as np
import networkx as nx, jgraph as ig
from random import randint
from collections import defaultdict
from itertools import tee, izip
from jgraph import *
from pylab import *
from pox.lib.revent import *


class GraphCliques(EventMixin):
    G = nx.Graph()

    def __init__(self):
        def startup():
            core.openflow.addListeners(self, priority=0)
            core.openflow_discovery.addListeners(self)
        core.call_when_ready(startup, ('openflow', 'openflow_discovery'))
        print
        "init completed"

    def _handle_LinkEvent(self, event):
        l = event.link
        sw1 = l.dpid1
        sw2 = l.dpid2
        pt1 = l.port1
        pt2 = l.port2
        self.G.add_node(sw1)
        self.G.add_node(sw2)

        if event.added:
            self.G.add_edge(sw1, sw2)

        if event.removed:
            try:
                self.G.remove_edge(sw1, sw2)

            except:
                print
                "remove edge error"
        try:
            # print nx.shortest_path(self.G,2,33)
            N = nx.number_of_nodes(self.G)
            print
            "Number of nodes", N
            E = nx.number_of_edges(self.G)
            print
            "Number of Edges", E

            if (N == 37) and (E == 57):
                print
                "Graph is ready now :-) "
                print
                "Graph nodes are: ", self.G.nodes()

                # nx.draw(self.G, with_labels=True)
                # plt.show()

        except:
            print
            "no such complete Graph yet..."

    # ---------------------------------------------------------
    # ---------------------------------------------------------

    def pt(self, g, membership=None):
        if membership is not None:
            gcopy = g.copy()
            edges = []
            edges_colors = []
            for edge in g.es():
                if membership[edge.tuple[0]] != membership[edge.tuple[1]]:
                    edges.append(edge)
                    edges_colors.append("gray")

                else:
                    edges_colors.append("black")

            gcopy.delete_edges(edges)
            layout = gcopy.layout("kk")
            g.es["color"] = edges_colors

        else:
            layout = g.layout("kk")
            g.es["color"] = "gray"
            visual_style = {}
            visual_style["vertex_label_dist"] = 0
            visual_style["vertex_shape"] = "circle"
            visual_style["edge_color"] = g.es["color"]
            # visual_style["bbox"] = (4000, 2500)

            visual_style["vertex_size"] = 30
            visual_style["layout"] = layout
            visual_style["bbox"] = (1024, 768)
            visual_style["margin"] = 40

            for vertex in g.vs():
                vertex["label"] = vertex.index

            if membership is not None:
                colors = []

                for i in range(0, max(membership) + 1):
                    colors.append('%06X' % randint(0, 0xFFFFFF))

                for vertex in g.vs():
                    vertex["color"] = str('#') + colors[membership[vertex.index]]

                visual_style["vertex_color"] = g.vs["color"]

            igraph.plot(g, **visual_style)


    def graph(self):
        """
        Draws the Graph/Network switches ...
        """
        # ---------------------------------------------------------

        N = self.G.nodes()
        d = defaultdict(list)
        E = self.G.number_of_edges()

        print
        "The number of Nodes in this Network:", N

        print
        "The number of Edges in this Network:", E

        fig = plt.figure()
        fig.canvas.set_window_title("The ERnet Topology View")
        nx.draw_networkx(self.G)
        plt.show()

        g = ig.Graph(len(self.G), zip(*zip(*nx.to_edgelist(self.G))[:2]))
        self.pt(g)
        cl = g.community_fastgreedy()

        # print cl
        membership = cl.as_clustering().membership

        print
        membership

        self.pt(g, membership)

        # print g.get_all_shortest_paths (2, 33)

        membership.pop(0)
        for q, a in zip(N, membership):
            print
            'The Node {0} --> Belongs to cluster {1}.'.format(q, a)

        # The following procedure is to get the exact nodes of each cluster
        for i in range(max(membership)):
            i += 1
            for j in range(len(N)):
                if membership[j] == i:
                    d[i].append(N[j])

        print
        d.items()

        # Test the subgraphs correctness, which is the clusters
        fig = plt.figure()
        fig.canvas.set_window_title("Sub-Graph/Clique 1 of ERnet")
        G3 = self.G.subgraph(d[1])  # each index in dictionary "d" is considered as a one cluster/subgraph of G
        nx.draw_networkx(G3)
        plt.show()
        # ---------------------------------------------------------


    def launch():
        core.registerNew(GraphCliques)
