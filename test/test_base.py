from base import BaseArc, BaseGraph, BaseNode


def test1():
    nodes = [BaseNode("1"), BaseNode("2"), BaseNode("3"), BaseNode("4")]
    arcs = [
            BaseArc(nodes[0], nodes[1]), BaseArc(nodes[0], nodes[2]),
            BaseArc(nodes[0], nodes[3]), BaseArc(nodes[1], nodes[2])
        ]

    graph = BaseGraph()

    for node in nodes:
        graph.add_node(node)
    for arc in arcs:
        graph.add_arc(arc)

    print(graph)