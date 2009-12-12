"""
    Unit tests for adjlist.
"""

from nose.tools import assert_equal

import networkx as nx

def test_read_multiline_adjlist_1():
    # Unit test for https://networkx.lanl.gov/trac/ticket/252
    s = """
        # New source node
        1 2
        # Neighbors list
        2 1
        3 1 
        """

    import StringIO
    strIO = StringIO.StringIO(s)

    G = nx.read_multiline_adjlist(strIO)
    adj = {'1': {'3': {}, '2': {}}, '3': {'1': {}}, '2': {'1': {}}}
    
    assert_equal(G.adj, adj)
    




