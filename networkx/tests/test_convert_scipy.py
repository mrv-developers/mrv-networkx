
import os, tempfile
from nose import SkipTest
from nose.tools import assert_raises, assert_true, assert_false

import networkx as nx
from networkx.generators.classic import barbell_graph,cycle_graph,path_graph

class TestConvertNumpy(object):
    @classmethod
    def setupClass(cls):
        global numpy, scipy
        try:
            import numpy
            import scipy
            import scipy.sparse
            # NetworkX uses a lazy import, so we need to use it to test it.
            numpy.__file__
            scipy.__file__
            scipy.sparse.__file__
        except ImportError:
            raise SkipTest('SciPy sparse library not available.')

    def __init__(self):
        self.G1 = barbell_graph(10, 3)
        self.G2 = cycle_graph(10, create_using=nx.DiGraph())

        self.G3 = self.create_weighted(nx.Graph())
        self.G4 = self.create_weighted(nx.DiGraph())

    def create_weighted(self, G):
        g = cycle_graph(4)
        e = g.edges()
        source = [u for u,v in e]
        dest = [v for u,v in e]
        weight = [s+10 for s in source]
        ex = zip(source, dest, weight)
        G.add_weighted_edges_from(ex)
        return G

    def assert_equal(self, G1, G2):
        assert_true( sorted(G1.nodes())==sorted(G2.nodes()) )
        assert_true( sorted(G1.edges())==sorted(G2.edges()) )

    def identity_conversion(self, G, A, create_using):
        GG = nx.from_scipy_sparse_matrix(A, create_using=create_using)
        self.assert_equal(G, GG)

        GW = nx.from_whatever(A, create_using=create_using)
        self.assert_equal(G, GW)

        GI = create_using.__class__(A)
        self.assert_equal(G, GI)

        ACSR = A.tocsr()
        GI = create_using.__class__(ACSR)
        self.assert_equal(G, GI)

        ACOO = A.tocoo()
        GI = create_using.__class__(ACOO)
        self.assert_equal(G, GI)

        ACSC = A.tocsc()
        GI = create_using.__class__(ACSC)
        self.assert_equal(G, GI)

        AD = A.todense()
        GI = create_using.__class__(AD)
        self.assert_equal(G, GI)

        AA = A.toarray()
        GI = create_using.__class__(AA)
        self.assert_equal(G, GI)

    def test_shape(self):
        "Conversion from non-square sparse array."
        A = scipy.sparse.lil_matrix([[1,2,3],[4,5,6]])
        assert_raises(nx.NetworkXError, nx.from_scipy_sparse_matrix, A)

    def test_identity_graph_matrix(self):
        "Conversion from graph to sparse matrix to graph."
        A = nx.to_scipy_sparse_matrix(self.G1)
        self.identity_conversion(self.G1, A, nx.Graph())

    def test_identity_digraph_matrix(self):
        "Conversion from digraph to sparse matrix to digraph."
        A = nx.to_scipy_sparse_matrix(self.G2)
        self.identity_conversion(self.G2, A, nx.DiGraph())

    def test_identity_weighted_graph_matrix(self):
        """Conversion from weighted graph to sparse matrix to weighted graph."""
        A = nx.to_scipy_sparse_matrix(self.G3)
        self.identity_conversion(self.G3, A, nx.Graph())

    def test_identity_weighted_digraph_matrix(self):
        """Conversion from weighted digraph to sparse matrix to weighted digraph."""
        A = nx.to_scipy_sparse_matrix(self.G4)
        self.identity_conversion(self.G4, A, nx.DiGraph())

    def test_nodelist(self):
        """Conversion from graph to sparse matrix to graph with nodelist."""
        P4 = path_graph(4)
        P3 = path_graph(3)
        A = nx.to_scipy_sparse_matrix(P4, nodelist=[0,1,2])
        GA = nx.Graph(A)    
        self.assert_equal(GA, P3)

    def test_altquery(self):
        """Conversion to sparse matrix using other edge attributes."""
        a = nx.MultiDiGraph()
        a.add_edge(1,1)
        a.add_edge(1,1,weight=.5)
        a.add_edge(1,2,height=30)
        a.add_edge(1,3)
        m = nx.to_scipy_sparse_matrix(a)
        m_ = numpy.matrix([[ 1.5 ,  1. ,  1.],
                           [ 0. ,  0. ,  0. ],
                           [ 0. ,  0. ,  0. ]], dtype=numpy.float32)
        assert_true(numpy.allclose(m.todense(), m_))

        m = nx.to_scipy_sparse_matrix(a, edge_attr=None)
        m_ = numpy.matrix([[ 2.,  1.,  1.],
                           [ 0.,  0.,  0.],
                           [ 0.,  0.,  0.]], dtype=numpy.float32)
        assert_true(numpy.allclose(m.todense(), m_))

        func = lambda x: sum([d.get('height',0) for d in x.values()])
        m = nx.to_scipy_sparse_matrix(a, edge_attr=func)
        m_ = numpy.matrix([[ 0.,  30.,  0.],
                           [ 0.,  0.,  0.],
                           [ 0.,  0.,  0.]], dtype=numpy.float32)
        assert_true(numpy.allclose(m.todense(), m_))

        func = lambda x: 1 if len(x) else 0
        m = nx.to_scipy_sparse_matrix(a, edge_attr=func)
        m_ = numpy.matrix([[ 1.,  1.,  1.],
                           [ 0.,  0.,  0.],
                           [ 0.,  0.,  0.]], dtype=numpy.float32)
        assert_true(numpy.allclose(m.todense(), m_))



