"""
Generators for some classic graphs.

The typical graph generator is called as follows:

>>> G=complete_graph(100)

returning the complete graph on n nodes labeled 0,..,99
as a simple graph. Except for empty_graph, all these generators return
a Graph class (i.e. a simple undirected graph).

"""
#    Copyright (C) 2004,2005 by 
#    Aric Hagberg <hagberg@lanl.gov>
#    Dan Schult <dschult@colgate.edu>
#    Pieter Swart <swart@lanl.gov>
#    Distributed under the terms of the GNU Lesser General Public License
#    http://www.gnu.org/copyleft/lesser.html
__author__ ="""Aric Hagberg (hagberg@lanl.gov)\nPieter Swart (swart@lanl.gov)"""
__date__ = "$Date: 2005-06-17 14:06:03 -0600 (Fri, 17 Jun 2005) $"
__credits__ = """"""
__revision__ = "$Revision: 1056 $"


#-------------------------------------------------------------------
#   Some Classic Graphs
#-------------------------------------------------------------------
import networkx
#from networkx.base import *
#from networkx.operators import *


def balanced_tree(r,h):
    """Return the perfectly balanced r-tree of height h.

    For r>=2, h>=1, this is the rooted tree where all leaves
    are at distance h from the root.
    The root has degree r and all other internal nodes have degree r+1.

    Graph order=1+r+r**2+...+r**h=(r**(h+1)-1)/(r-1), graph size=order-1.

    Node labels are integers numbered 0 (the root) up to order-1.
    
    """
    if r<2:
        raise networkx.NetworkXError, \
              "Invalid graph description, r should be >=2"
    if h<1:
        raise networkx.NetworkXError, \
              "Invalid graph description, h should be >=1"
    
    G=empty_graph(0)
    G.name="balanced tree"

    # grow tree of increasing height by repeatedly adding a layer
    # of new leaves to current leaves
    
    # first create root of degree r
    root=0
    v=root
    G.add_node(v)
    newleavelist=[]
    i=0
    while i < r:
        v=v+1
        G.add_edge(root,v)
        newleavelist.append(v)
        i=i+1
    #   all other  internal nodes have degree r+1
    height=1
    while height<h:
        leavelist=newleavelist[:]
        newleavelist=[]
        for leave in leavelist:
            for i in xrange(r):
                v=v+1
                G.add_edge(leave,v)
                newleavelist.append(v)
        height=height+1
    return G

def barbell_graph(m1,m2):
    """Return the Barbell Graph: two complete graphs connected by a path.

    For m1>1 and m2>=0.

    Two complete graphs K_{m1} form the left and right bells,
    and are connected by a path P_{m2}.

    The 2*m1+m2  nodes are numbered
        0,...,m1-1 for the left barbell,
        m1,...,m1+m2-1 for the path,
        and m1+m2,...,2*m1+m2-1 for the right barbell.

    The 3 subgraphs are joined via the edges (m1-1,m1) and (m1+m2-1,m1+m2).
    If m2=0, this is merely two complete graphs joined together.

    This graph is an extremal example in David Aldous
    and Jim Fill's etext on Random Walks on Graphs.

    """
    if m1<2:
        raise networkx.NetworkXError, \
              "Invalid graph description, m1 should be >=2"
    if m2<0:
        raise networkx.NetworkXError, \
              "Invalid graph description, m2 should be >=0"

    # left barbell
    G=complete_graph(m1)
    G.name="barbell graph (%d,%d)"%(m1,m2)
    
    # connecting path
    G.add_nodes_from([v for v in range(m1,m1+m2-1)])
    if m2>1:
        G.add_edges_from([(v,v+1) for v in range(m1,m1+m2-1)])
    # right barbell
#    G.add_nodes_from([v for v in range(m1+m2,2*m1+m2)])
    for u in range(m1+m2,2*m1+m2):
        for v in range(u,2*m1+m2):
            G.add_edge(u,v)
    # connect it up
    G.add_edge(m1-1,m1)
    if m2>0:
        G.add_edge(m1+m2-1,m1+m2)
    return G

def complete_graph(n):
    """ Return the Complete graph K_n with n nodes. """
    G=empty_graph(n)
    G.name="complete graph K_%d"%n
    for u in xrange(n):
        for v in xrange(u,n):
            G.add_edge(u,v)
    return G

def complete_bipartite_graph(n1,n2):
    """Return the complete bipartite graph K_{n1_n2}.
    
    Contains n1 nodes in the first subgraph and n2 nodes
    in the second subgraph.
    
    """
    G=empty_graph(n1+n2)
    G.name="complete bipartite graph"
    for v1 in xrange(n1):
        for v2 in xrange(n2):
            G.add_edge(v1,n1+v2)
    return G

def circular_ladder_graph(n):
    """Return the circular ladder graph CL_n of length n.

    CL_n consists of two concentric n-cycles in which
    each of the n pairs of concentric nodes are joined by an edge.
    
    """
    G=ladder_graph(n)
    G.name="Circular Ladder Graph"
    G.add_edge(0,n-1)
    G.add_edge(n,2*n-1)
    return G

def cycle_graph(n):
    """Return the cycle graph C_n over n nodes.
   
    C_n is P_n with two end-nodes connected.
    
    """
    G=path_graph(n)
    G.name="cycle graph (%d)"%n
    if n>1: G.add_edge(0,n-1)
    return G

def dorogovtsev_goltsev_mendes_graph(n):
    """Return the hierarchically constructed Dorogovtsev-Goltsev-Mendes graph.

    n is the generation.
    See: arXiv:/cond-mat/0112143 by Dorogovtsev, Goltsev and Mendes.
    
    """
    G=networkx.Graph()
    G.name="Dorogovtsev-Goltsev-Mendes Graph"
    G.add_edge(0,1)
    if n==0:
        return G
    new_node = 2         # next node to be added
    for i in range(1,n+1): #iterate over number of generations.
        last_generation_edges = G.edges()
        number_of_edges_in_last_generation = len(last_generation_edges)
        for j in range(0,number_of_edges_in_last_generation):
            G.add_edge(new_node,last_generation_edges[j][0])
            G.add_edge(new_node,last_generation_edges[j][1])
            new_node += 1
    return G

def empty_graph(n=0,create_using=None,**kwds):
    """
    Return the empty graph with n nodes
    (with integer labels 0,...,n-1) and zero edges.

    >>> G=empty_graph(n) 

    The variable create_using should point to a "graph"-like object that
    will be cleaned (nodes and edges will be removed) and refitted as
    an empty "graph" with n nodes with integer labels. This capability
    is useful for specifying the class-nature of the resulting empty
    "graph" (i.e. Graph, DiGraph, MyWeirdGraphClass, etc.).
    
    Firstly, the variable create_using can be used to create an
    empty digraph, network,etc.  For example,

    >>> G=empty_graph(n,create_using=DiGraph())

    will create an empty digraph on n nodes, and

    >>> G=empty_graph(n,create_using=DiGraph())

    will create an empty digraph on n nodes.

    Secondly, one can pass an existing graph (digraph, pseudograph,
    etc.) via create_using. For example, if G is an existing graph
    (resp. digraph, pseudograph, etc.), then empty_graph(n,create_using=G)
    will empty G (i.e. delete all nodes and edges using G.clear() in
    baseNX) and then add n nodes and zero edges, and return the modified
    graph (resp. digraph, pseudograph, etc.).

    WARNING: The graph dna is not scrubbed in this process.

    See also create_empty_copy(G).
    
    """
    if create_using is None:
        # default empty graph is a simple graph
        G=networkx.Graph(**kwds)
    else:
        G=create_using
        G.clear()

    G.add_nodes_from(xrange(n))
    G.name="empty graph" 
    return G

def grid_2d_graph(m,n):
    """ Return the 2d grid graph of mxn nodes,
        each connected to its nearest neighbors.
    """
    G=empty_graph(0)
    G.name="grid 2d graph"
    rows=range(m)
    columns=range(n)
    def _label(i,j):
        return i*n+j
    for i in rows:
        for j in columns:
            G.add_node( _label(i,j) )
    for i in rows:
        for j in columns:
            if i>0: G.add_edge( _label(i,j), _label(i-1,j) )
            if i<m-1: G.add_edge( _label(i,j), _label(i+1,j) )
            if j>0: G.add_edge( _label(i,j), _label(i,j-1) )
            if j<n-1: G.add_edge( _label(i,j), _label(i,j+1) )
    return G


def grid_graph(dim,periodic=False):
    """ Return the n-dimensional grid graph.

    The dimension is the length of the list 'dim' and the
    size in each dimension is the value of the list element.

    E.g. G=grid_graph(dim=[2,3]) produces a 2x3 grid graph.

    If periodic=True then join grid edges with periodic boundary conditions.
    """    
    from networkx.utils import is_list_of_ints
    if not isinstance(dim,list):
        raise TypeError,"dim is not a list"
    if dim==[]:
        G=networkx.Graph()
        G.name="grid graph"
        return G
    if not is_list_of_ints(dim):
        raise networkx.NetworkXError,"dim is not a list of integers"
    if min(dim)<=0:
        raise networkx.NetworkXError,\
              "dim is not a list of strictly positive integers"       
    if periodic:
        func=cycle_graph
    else:
        func=path_graph

    current_dim=dim.pop()
    G=func(current_dim)
    while len(dim)>0:
        current_dim=dim.pop() 
        Gnew=func(current_dim)
        Gold=G.copy()
        G=networkx.operators.cartesian_product(Gnew,Gold)
    # graph G is done but has labels of the form (1,(2,(3,1)))
    # so relabel
    # this works but loses the info from each dimension
    H=networkx.operators.convert_node_labels_to_integers(G)
    H.name="Grid Graph"
    return H

def hypercube_graph(n):
    """return the n-dimensional hypercube."""
    dim=n*[2]
    G=grid_graph(dim)
    G.name="hypercube graph (%d)"%n
    return G

def ladder_graph(n):
    """Return the Ladder graph of length n.

    This is two rows of n nodes,
    each pair connected by a single edge.
    
    """
    G=empty_graph(2*n)
    G.name="ladder graph (%d)"%n 
    G.add_edges_from([(v,v+1) for v in xrange(n-1)])
    G.add_edges_from([(v,v+1) for v in xrange(n,2*n-1)])
    G.add_edges_from([(v,v+n) for v in xrange(n)])
    return G

def lollipop_graph(m,n):
    """Return the Lollipop Graph; K_m connected to P_n.

    This is the Barbell Graph without the right barbell.

    For m>1 and n>=0, the complete graph K_m is connected to the 
    path P_n.  The resulting m+n nodes are labelled 0,...,m-1 for the
    complete graph and m,...,m+n-1 for the path. The 2 subgraphs
    are joined via the edge (m-1,m).  If n=0, this is merely a complete 
    graph.

    (This graph is an extremal example in David Aldous and Jim
    Fill's etext on Random Walks on Graphs.)
    
    """
    if m<2:
        raise networkx.NetworkXError, \
              "Invalid graph description, m should be >=2"
    if n<0:
        raise networkx.NetworkXError, \
              "Invalid graph description, n should be >=0"
    # complete graph
    G=complete_graph(m)
    G.name="lollipop graph (%d,%d)"%(m,n)
    # the stick
    G.add_nodes_from([v for v in xrange(m,m+n)])
    if n>1:
        G.add_edges_from([(v,v+1) for v in xrange(m,m+n-1)])
    # connect ball to stick
    if m>0: G.add_edge(m-1,m)
    return G

def null_graph(create_using=None,**kwds):
    """ Return the Null graph with no nodes or edges. """
    G=empty_graph(0,create_using,**kwds)
    G.name="null graph"
    return G

def path_graph(n):
    """Return the Path graph P_n of n nodes linearly connected
    by n-1 edges.
    """
    G=empty_graph(n)
    G.name="path graph (%d)"%n
    G.add_edges_from([(v,v+1) for v in xrange(n-1)])
    return G

def periodic_grid_2d_graph(m,n):
    """
    Return the 2-D Grid Graph of mxn nodes,
    each connected to its nearest neighbors.

    Boundary nodes are identified in a periodic fashion.
    
    """
    G=grid_2d_graph(m,n)  # plain grid graph
    def _label(i,j):
        return i*n+j
    # make it periodic
    rows=range(m)
    columns=range(n)
    for i in rows:
        G.add_edge(_label(i,0), _label(i,n-1))
    for j in columns:
        G.add_edge(_label(0,j), _label(m-1,j))
    G.name="periodic grid 2d graph"
    return G        


def star_graph(n):
    """ Return the Star graph with n+1 nodes:
        one center node, connected to n outer nodes.
    """
    G=complete_bipartite_graph(1,n)
    G.name="star graph (%d)"%n
    return G

def trivial_graph():
    """ Return the Trivial graph with one node (with integer label 0)
    and no edges.
    """
    G=empty_graph(1)
    G.name="trivial graph"
    return G

def wheel_graph(n):
    """ Return the wheel graph: a single hub node connected
    to each node of the (n-1)-node cycle graph. 
    """
    G=star_graph(n-1)
    G.name="wheel graph (%d)"%n
    G.add_edges_from([(v,v+1) for v in xrange(1,n-1)])
    if n>1:
        G.add_edge(1,n-1)
    return G
                        

def _test_suite():
    import doctest
    suite = doctest.DocFileSuite('tests/generators/classic.txt',
                                 package='networkx')
    return suite


if __name__ == "__main__":
    import os
    import sys
    import unittest
    if sys.version_info[:2] < (2, 4):
        print "Python version 2.4 or later required (%d.%d detected)."\
              %  sys.version_info[:2]
        sys.exit(-1)
    # directory of networkx package (relative to this)
    nxbase=sys.path[0]+os.sep+os.pardir
    sys.path.insert(0,nxbase) # prepend to search path
    unittest.TextTestRunner().run(_test_suite())
    
