#!/usr/bin/env python
"""
An example using networkx.XGraph().

miles_graph() returns an undirected graph over the 128 US cities from
the datafile miles.dat. The cities each have location and population
data.  The edges are labeled with the distance betwen the two cities.

This example is described in Section 1.1 in Knuth's book [1,2].

References.
-----------

[1] Donald E. Knuth,
    "The Stanford GraphBase: A Platform for Combinatorial Computing",
    ACM Press, New York, 1993.
[2] http://www-cs-faculty.stanford.edu/~knuth/sgb.html


"""
__author__ = """Aric Hagberg (hagberg@lanl.gov)"""
__date__ = "$Date: 2005-04-01 14:20:02 -0700 (Fri, 01 Apr 2005) $"
__credits__ = """"""
__revision__ = ""
#    Copyright (C) 2004 by 
#    Aric Hagberg <hagberg@lanl.gov>
#    Dan Schult <dschult@colgate.edu>
#    Pieter Swart <swart@lanl.gov>
#    Distributed under the terms of the GNU Lesser General Public License
#    http://www.gnu.org/copyleft/lesser.html

def miles_graph():
    """ Return the cites example graph in miles.dat
        from the Stanford GraphBase.
    """
    try:
        fh=open("miles.dat","r")
    except IOError:
        print "miles.dat not found"
        raise

    G=XGraph()
    G.position={}
    G.population={}

    cities=[]
    for line in fh.readlines():
        if line.startswith("*"): # skip comments
            continue

        numfind=re.compile("^\d+") 

        if numfind.match(line): # this line is distances
            dist=line.split()
            for d in dist:
                G.add_edge(city,cities[i],int(d))
                i=i+1
        else: # this line is a city, position, population
            i=1
            (city,coordpop)=line.split("[")
            cities.insert(0,city)
            (coord,pop)=coordpop.split("]")
            (y,x)=coord.split(",")
        
            G.add_node(city)
            # assign position - flip x axis for matplotlib, shift origin
            G.position[city]=(-int(x)+7500,int(y)-3000)
            G.population[city]=float(pop)/1000.0
    return G            

if __name__ == '__main__':
    from networkx import *
    import re
    import sys

    G=miles_graph()

    print "Loaded Donald Knuth's miles.dat containing 128 cities."
    print "digraph has %d nodes with %d edges"\
          %(number_of_nodes(G),number_of_edges(G))


    # make new graph of cites, edge if less then 300 miles between them
    H=Graph()
    for v in G:
        H.add_node(v)
    for (u,v,d) in G.edges():
        if d < 300:
            H.add_edge(u,v)

    # draw with matplotlib/pylab            

    # with nodes colored by population, no labels
    # draw_nx(H,G.position,node_labels=False,node_size=80,node_color=G.population,cmap=cm.jet)
    # with nodes sized py population
    # draw_nx(H,G.position,node_labels=False,node_size=G.population,cmap=cm.jet)
    draw_nx(H,G.position,node_labels=False,node_size=G.population,node_color=H.degree(with_labels=True),cmap=cm.jet)
    savefig("miles.png")
    # with nodes colored by degree
    #draw_nx(H,G.position,node_labels=False,node_size=50,node_color=H.degree(with_labels=True),cmap=cm.jet)
 



