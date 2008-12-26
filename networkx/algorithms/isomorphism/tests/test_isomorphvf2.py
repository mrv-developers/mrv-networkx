"""
    Tests for VF2 isomorphism algorithm.
"""

import os
import struct
import random

from nose.tools import assert_true
import networkx as nx
import networkx.algorithms.isomorphism.isomorphvf2 as vf2

class TestWikipediaExample(object):
    # Source: http://en.wikipedia.org/wiki/Graph_isomorphism

    # Nodes 'a', 'b', 'c' and 'd' form a column.
    # Nodes 'g', 'h', 'i' and 'j' form a column.
    g1edges = [['a','g'], ['a','h'], ['a','i'], 
               ['b','g'], ['b','h'], ['b','j'], 
               ['c','g'], ['c','i'], ['c','j'], 
               ['d','h'], ['d','i'], ['d','j']]

    # Nodes 1,2,3,4 form the clockwise corners of a large square.
    # Nodes 5,6,7,8 form the clockwise corners of a small square 
    g2edges = [[1,2], [2,3], [3,4], [4,1], 
               [5,6], [6,7], [7,8], [8,5], 
               [1,5], [2,6], [3,7], [4,8]]

    def test_graph(self):
        g1 = nx.Graph()
        g2 = nx.Graph()
        g1.add_edges_from(self.g1edges)
        g2.add_edges_from(self.g2edges)
        gm = vf2.GraphMatcher(g1,g2)
        assert_true(gm.is_isomorphic())

        mapping = gm.mapping.items()
        mapping.sort()
        isomap = [('a', 1), ('b', 6), ('c', 3), ('d', 8), 
                  ('g', 2), ('h', 5), ('i', 4), ('j', 7)]
        assert_true(mapping==isomap)
        
    def test_subgraph(self):
        g1 = nx.Graph()
        g2 = nx.Graph()
        g1.add_edges_from(self.g1edges)
        g2.add_edges_from(self.g2edges)
        g3 = g2.subgraph([1,2,3,4])
        gm = vf2.GraphMatcher(g1,g3)
        assert_true(gm.subgraph_is_isomorphic())

class TestVF2GraphDB(object):
    # http://amalfi.dis.unina.it/graph/db/

    @staticmethod
    def create_graph(filename):
        """Creates a Graph instance from the filename."""

        # The file is assumed to be in the format from the VF2 graph database.
        # Each file is composed of 16-bit numbers (unsigned short int).
        # So we will want to read 2 bytes at a time.

        # We can read the number as follows:
        #   number = struct.unpack('<H', file.read(2))
        # This says, expect the data in little-endian encoding
        # as an unsigned short int and unpack 2 bytes from the file.

        fh = open(filename, mode='rb')

        # Grab the number of nodes.
        # Node numeration is 0-based, so the first node has index 0.
        nodes = struct.unpack('<H', fh.read(2))[0]

        graph = nx.Graph()
        for from_node in xrange(nodes):
            # Get the number of edges.
            edges = struct.unpack('<H', fh.read(2))[0]
            for edge in xrange(edges):
                # Get the terminal node.
                to_node = struct.unpack('<H', fh.read(2))[0]
                graph.add_edge(from_node, to_node)

        fh.close()
        return graph

    def test_graph(self):
        head,tail = os.path.split(__file__)
        g1 = self.create_graph(os.path.join(head,'iso_r01_s80.A99'))
        g2 = self.create_graph(os.path.join(head,'iso_r01_s80.B99'))
        gm = vf2.GraphMatcher(g1,g2)
        assert_true(gm.is_isomorphic())

    def test_subgraph(self):
        # A is the subgraph
        # B is the full graph
        head,tail = os.path.split(__file__)
        subgraph = self.create_graph(os.path.join(head,'si2_b06_m200.A99'))
        graph = self.create_graph(os.path.join(head,'si2_b06_m200.B99'))
        gm = vf2.GraphMatcher(graph, subgraph)
        assert_true(gm.subgraph_is_isomorphic())

def test_graph_atlas():
    Atlas = nx.graph_atlas_g()[0:208] # 208, 6 nodes or less
    alphabet = range(26)
    for graph in Atlas:
        nlist = graph.nodes()
        labels = alphabet[:len(nlist)]
        for s in range(10):
            random.shuffle(labels)
            d = dict(zip(nlist,labels))
            relabel = nx.relabel_nodes(graph, d)
            gm = vf2.GraphMatcher(graph, relabel)
            assert_true(gm.is_isomorphic())

def test_multiedge():
    # Simple test for multigraphs
    # Need something much more rigorous
    edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), 
             (5, 6), (6, 7), (7, 8), (8, 9), (9, 10), 
             (10, 11), (10, 11), (11, 12), (11, 12), 
             (12, 13), (12, 13), (13, 14), (13, 14), 
             (14, 15), (14, 15), (15, 16), (15, 16), 
             (16, 17), (16, 17), (17, 18), (17, 18), 
             (18, 19), (18, 19), (19, 0), (19, 0)]
    nodes = range(20)

    for g1 in [nx.MultiGraph(), nx.MultiDiGraph()]:
        g1.add_edges_from(edges)
        for _ in range(50):
            new_nodes = list(nodes)
            random.shuffle(new_nodes)
            d = dict(zip(nodes, new_nodes))
            g2 = nx.relabel_nodes(g1, d)
            if not g1.directed:
                gm = vf2.GraphMatcher(g1,g2)
            else:
                gm = vf2.DiGraphMatcher(g1,g2)
            assert_true(gm.is_isomorphic())

def test_selfloop():
    # Simple test for graphs with selfloops
    edges = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 2), 
             (2, 4), (3, 1), (3, 2), (4, 2), (4, 5), (5, 4)]
    nodes = range(6)

    for g1 in [nx.Graph(), nx.DiGraph()]:
        g1.add_edges_from(edges)
        for _ in range(100):
            new_nodes = list(nodes)
            random.shuffle(new_nodes)
            d = dict(zip(nodes, new_nodes))
            g2 = nx.relabel_nodes(g1, d)
            if not g1.directed:
                gm = vf2.GraphMatcher(g1,g2)
            else:
                gm = vf2.DiGraphMatcher(g1,g2)
            assert_true(gm.is_isomorphic())
                
