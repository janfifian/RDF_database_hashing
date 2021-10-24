import copy
import pytest
import RDF
import RDF_graph_Gen
from itertools import groupby

def all_equal(iterable): ##A fast method of checking if list elements are all equal
    g = groupby(iterable)
    return next(g, True) and not next(g, False)

def test_hashes_of_same_database_in_different_order_should_remain_same():
    hashes = []
    for i in range(1, 4):
        f = open(".\\testfiles\\acyclic_rdf_base_with_multiple_edges" + str(i) + ".txt", "r")
        RDFgraph_1 = RDF.read_RDF_graph(f.read().split('\n'))
        BG_1 = copy.deepcopy(RDFgraph_1.blanks)
        assert not (RDF.cycle_detection(BG_1, RDFgraph_1))
        hashes.append(RDF.hash_database(RDFgraph_1))
        f.close()
    assert all_equal(hashes)

def test_hashes_of_distinct_databases_should_not_be_same():
    f = open(".\\testfiles\\acyclic_rdf_base_with_multiple_edges_and_2_real_vertices.txt", "r")
    g = open(".\\testfiles\\acyclic_rdf_base_with_multiple_edges_and_2_real_vertices_attached_somewhere_else.txt", "r")
    h = open(".\\testfiles\\acyclic_rdf_base_with_multiple_edges_and_2_real_vertices_and_real_edge.txt", "r")
    RDFgraph_1 = RDF.read_RDF_graph(f.read().split('\n'))
    RDFgraph_2 = RDF.read_RDF_graph(g.read().split('\n'))
    RDFgraph_3 = RDF.read_RDF_graph(h.read().split('\n'))
    H1=RDF.hash_database(RDFgraph_1)
    H2=RDF.hash_database(RDFgraph_2)
    H3=RDF.hash_database(RDFgraph_3)
    assert (H1!=H2)
    assert (H3!=H2)
    assert (H1!=H3)
    f.close()
    g.close()
    h.close()

def test_randomly_generated_RDF_file_should_be_readable_and_acyclic_and_hashable():
    R = RDF_graph_Gen.generate_random_RDF_graph(number_of_blanks=5, number_of_ground_nodes=5, number_of_BG_edges=8,
                                  number_of_grounded_edges=5, ratio=0.7)
    R.to_file(".\\testfiles\\Randomly_generated_graph.txt")
    f = open(".\\testfiles\\Randomly_generated_graph.txt", "r")
    RDFgraph = RDF.read_RDF_graph(f.read().split('\n'))
    BG = copy.deepcopy(RDFgraph.blanks)
    assert not (RDF.cycle_detection(BG))
    assert (len(RDF.hash_database(RDFgraph))>=0)
    f.close()

def test_case_1_two_new_grounded_nodes():
    e = open(".\\testfiles\\Incrementation_testing_case_1_1.txt", "r")
    f = open(".\\testfiles\\Incrementation_testing_case_1_1a.txt", "r")
    RDFgraph = RDF.read_RDF_graph(e.read().split('\n'))
    b4increment = RDF.hash_database(RDFgraph)
    print(b4increment)
    RDFgraph.hash_increment_triple("Ania\tLubi\tHanna")
    RDFgraph2 = RDF.read_RDF_graph(f.read().split('\n'))
    afterincrement = RDF.hash_database(RDFgraph2)
    assert (afterincrement==RDFgraph.hash_value)
    e.close()
    f.close()

def test_case_1_one_new_grounded_node_variant_one():
    e = open(".\\testfiles\\Incrementation_testing_case_1_1.txt", "r")
    f = open(".\\testfiles\\Incrementation_testing_case_1_1b.txt", "r")
    RDFgraph = RDF.read_RDF_graph(e.read().split('\n'))
    b4increment = RDF.hash_database(RDFgraph)
    RDFgraph.hash_increment_triple("blank5Anon\tKnows\tRandomPerson")
    RDFgraph2 = RDF.read_RDF_graph(f.read().split('\n'))
    afterincrement = RDF.hash_database(RDFgraph2)
    assert (afterincrement==RDFgraph.hash_value)
    e.close()
    f.close()

def test_case_1_two_new_blank_nodes():
    e = open(".\\testfiles\\Incrementation_testing_case_1_1.txt", "r")
    f = open(".\\testfiles\\Incrementation_testing_case_1_1c.txt", "r")
    RDFgraph = RDF.read_RDF_graph(e.read().split('\n'))
    b4increment = RDF.hash_database(RDFgraph)
    RDFgraph3 = copy.deepcopy(RDFgraph)
    RDFgraph.hash_increment_triple("blank6Anonida\tLaughs_at\tblank5Anon")
    RDFgraph3.hash_increment_triple("blank7Ananias\tLaughs_at\tblank19Debilus")
    RDFgraph2 = RDF.read_RDF_graph(f.read().split('\n'))
    afterincrement = RDF.hash_database(RDFgraph2)
    assert (afterincrement == RDFgraph.hash_value)
    assert (afterincrement == RDFgraph3.hash_value)
    e.close()
    f.close()

def test_case_1_one_new_grounded_node_variant_two():
    e = open(".\\testfiles\\Incrementation_testing_case_1_1.txt", "r")
    f = open(".\\testfiles\\Incrementation_testing_case_1_1d.txt", "r")
    RDFgraph = RDF.read_RDF_graph(e.read().split('\n'))
    b4increment = RDF.hash_database(RDFgraph)
    RDFgraph.hash_increment_triple("RandomPerson\tKnows\tblank5Anon")
    RDFgraph2 = RDF.read_RDF_graph(f.read().split('\n'))
    afterincrement = RDF.hash_database(RDFgraph2)
    assert (afterincrement == RDFgraph.hash_value)
    e.close()
    f.close()

def test_case_1_two_existing_grounded_nodes():
    e = open(".\\testfiles\\Incrementation_testing_case_1_1.txt", "r")
    f = open(".\\testfiles\\Incrementation_testing_case_1_1e.txt", "r")
    RDFgraph = RDF.read_RDF_graph(e.read().split('\n'))
    b4increment = RDF.hash_database(RDFgraph)
    RDFgraph.hash_increment_triple("JamesVQ0LQ71\tKnows\tEmmaIBM3773")
    RDFgraph2 = RDF.read_RDF_graph(f.read().split('\n'))
    afterincrement = RDF.hash_database(RDFgraph2)
    assert (afterincrement == RDFgraph.hash_value)
    e.close()
    f.close()

def test_case_1_one_existing_grounded_node_variant_one():
    e = open(".\\testfiles\\Incrementation_testing_case_1_1.txt", "r")
    f = open(".\\testfiles\\Incrementation_testing_case_1_1f.txt", "r")
    RDFgraph = RDF.read_RDF_graph(e.read().split('\n'))
    b4increment = RDF.hash_database(RDFgraph)
    RDFgraph.hash_increment_triple("JamesVQ0LQ71\tKnows\tAnia")
    RDFgraph2 = RDF.read_RDF_graph(f.read().split('\n'))
    afterincrement = RDF.hash_database(RDFgraph2)
    assert (afterincrement == RDFgraph.hash_value)
    e.close()
    f.close()

def test_case_1_one_existing_grounded_node_variant_two():
    e = open(".\\testfiles\\Incrementation_testing_case_1_1.txt", "r")
    f = open(".\\testfiles\\Incrementation_testing_case_1_1g.txt", "r")
    RDFgraph = RDF.read_RDF_graph(e.read().split('\n'))
    b4increment = RDF.hash_database(RDFgraph,Debug=True)
    RDFgraph.hash_increment_triple("Ania\tKnows\tEmmaIBM3773")
    RDFgraph2 = RDF.read_RDF_graph(f.read().split('\n'))
    afterincrement = RDF.hash_database(RDFgraph2,Debug=True)
    assert (afterincrement == RDFgraph.hash_value)
    e.close()
    f.close()

def test_case_1_one_existing_grounded_node_variant_three():
    e = open(".\\testfiles\\Incrementation_testing_case_1_1.txt", "r")
    f = open(".\\testfiles\\Incrementation_testing_case_1_1h.txt", "r")
    RDFgraph = RDF.read_RDF_graph(e.read().split('\n'))
    b4increment = RDF.hash_database(RDFgraph)
    RDFgraph.hash_increment_triple("blank6Mama\tKnows\tEmmaIBM3773")
    RDFgraph2 = RDF.read_RDF_graph(f.read().split('\n'))
    afterincrement = RDF.hash_database(RDFgraph2)
    assert (afterincrement == RDFgraph.hash_value)
    e.close()
    f.close()

def test_case_1_one_existing_grounded_node_variant_four():
    e = open(".\\testfiles\\Incrementation_testing_case_1_1.txt", "r")
    f = open(".\\testfiles\\Incrementation_testing_case_1_1i.txt", "r")
    RDFgraph = RDF.read_RDF_graph(e.read().split('\n'))
    RDF.hash_database(RDFgraph)
    RDFgraph.hash_increment_triple("JamesVQ0LQ71\tKnows\tblank6Mama")
    RDFgraph2 = RDF.read_RDF_graph(f.read().split('\n'))
    afterincrement = RDF.hash_database(RDFgraph2)
    assert (afterincrement == RDFgraph.hash_value)
    e.close()
    f.close()

def test_hashstring():
    assert not (RDF.hashstring("Ania") == RDF.hashstring("Hania"))


