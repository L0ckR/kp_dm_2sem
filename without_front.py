from pprint import pprint
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import itertools
def parse_graph(graph_edges_list):
    nodes = []
    income = {}
    outcome = {}
    for i,j in graph_edges_list:
        outcome [i]  = outcome.get(i, []) + [j]
        income [j] = income.get(j, []) + [i]
        if not i in nodes :
            nodes += [i]
        if not j in nodes :
            nodes += [j]
    return (nodes, income, outcome)

def is_tree(graph_edges_list, root):
    nodes, income, outcome = parse_graph(graph_edges_list)
    if sum( [ len(j) for j in outcome.values() ] )!=len(nodes) -1 :
        return False

    def visit_outcome(r, visited):
        if r in visited:
            return False;
        visited += [r]
        if r in outcome:
            for j in outcome[r]:
                if not visit_outcome(j, visited):
                    return False
        return True

    visited = []
    if not visit_outcome(root, visited):
        return False
    return sorted(visited)==sorted(nodes)


def clusters_join(clusters, a, b ):
    clustter_a = [ i for i in clusters if a in i ][0]
    clustter_b = [ i for i in clusters if b in i ][0]
    if clustter_a != clustter_b :
        return [ i for i in clusters if (a not in i) and (b not in i) ] + [ clustter_a + clustter_b ]
    else:
        return [i for i in clusters]

def clusters_check(clusters, a, b ):
    for i in clusters :
        if a in i :
            return not (b in i)
    return False

def seek_subtree(graph_eidges_list):
    nodes, income, outcome = parse_graph(graph_eidges_list)
    result = []

    possible_roots = [ i for i in nodes if not i in income ]
    if len(possible_roots) >1 :
        return [] # no solutions.
    if len(possible_roots) ==0 :
        possible_roots = [i for i in nodes]

    for root in possible_roots:
        non_root_nodex = [ i for i in nodes if i!=root ]
        non_root_nodex = sorted( non_root_nodex, key = lambda i : len(income[i]) )

        clusters = nodes.copy()

        def visit_left_node( left_nodes, clusters, eidges ):
            if len(left_nodes) == 0 :
                if is_tree(eidges, root):
                    return [ eidges ]
            else:
                b = left_nodes[0]
                result = []
                for a in income[b]:
                    if clusters_check(clusters, a, b):
                        result += visit_left_node( left_nodes[1:], clusters_join(clusters, a,b),  eidges+[a+b],  )
                return result

        result  = visit_left_node( non_root_nodex, nodes, []  )

    return result
                
def count_trees(n, ar):
    d = np.asarray([[sum([ar[k][i] for k in range(n)]) if i==j else 0 for j in range(n) ] for i in range(n)])
    b = d - ar
    s = 0
    for i in range(n):
        s += round(np.linalg.det(minor(b, i, i)))
    print(s)

def minor(arr,i,j):
    # ith row, jth column removed
    return arr[np.array(list(range(i))+list(range(i+1,arr.shape[0])))[:,np.newaxis],
               np.array(list(range(j))+list(range(j+1,arr.shape[1])))]

if __name__ == '__main__':
    matrix = [[0, 1, 0, 0, 1],
              [0, 0, 1, 0, 1],
              [0, 0, 0, 1, 0],
              [0, 0, 1, 0, 0],
              [0, 1, 0, 1, 0]]
    ar = np.asarray(matrix)
    graph = nx.DiGraph(ar)
    graph = nx.relabel_nodes(graph, {k:chr(k+65) for k in graph.nodes})
    # plt.figure("ГРаф G")
    # nx.draw(graph, with_labels=True)
    # i = 1
    pra = seek_subtree([''.join(i) for i in graph.edges])
    print(pra)
    # for pratree in pra:
    #     gr = nx.DiGraph()
    #     gr.add_edges_from([tuple(list(i)) for i in pratree])
    #     plt.figure("Прадерево №"+str(i))
    #     nx.draw(gr, with_labels=True)
    #     i += 1
    # plt.show()
    # print(count_trees(5, matrix) if -1 else 0)