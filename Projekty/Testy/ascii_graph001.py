from ascii_graph import Pyasciigraph
from ascii_graph import colors

import collections
from _collections_abc import Iterable
collections.Iterable = Iterable


data = [ ("A", 15, colors.BICya), ("B", 6,colors.BBla), ("C", 4,colors.BGre  ), ("D", 7, colors.BBla) ]

# Most simple graph
graph = Pyasciigraph()
for line in graph.graph('Graph title', data):
    print(line)