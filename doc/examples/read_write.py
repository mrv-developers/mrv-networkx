#!/usr/bin/env python
"""
Read and write graphs.
"""
__author__ = """Aric Hagberg (hagberg@lanl.gov)"""
#    Copyright (C) 2004-2006 by 
#    Aric Hagberg <hagberg@lanl.gov>
#    Dan Schult <dschult@colgate.edu>
#    Pieter Swart <swart@lanl.gov>
#    Distributed under the terms of the GNU Lesser General Public License
#    http://www.gnu.org/copyleft/lesser.html

from networkx import *
import sys
G=grid_2d_graph(5,5)  # 5x5 grid
write_adjlist(G,sys.stdout) # write adjacency list to screen
# write edgelist to grid.edgelist
write_edgelist(G,path="grid.edgelist",delimiter=":") 
# read edgelist from grid.edgelist
H=read_edgelist(path="grid.edgelist",delimiter=":") 

