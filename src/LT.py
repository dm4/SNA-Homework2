#!/usr/bin/env python

import networkx as nx
from collections import deque

def bfs(G, queue, infected_node_num):
    while len(queue) > 0:
        node = queue.popleft()
        for nb in G.successors(node):
            if G.node[nb]['infected']:
                continue
            else:
                # chekc the neighbors
                all_in_node = G.in_degree(nb)
                infected_in_node = 0
                for in_node in G.predecessors(nb):
                    if G.node[in_node]['infected']:
                        infected_in_node += 1

                # check should be infected
                if float(infected_in_node)/float(all_in_node) >= 0.3:
                    G.node[nb]['infected'] = True
                    infected_node_num += 1
                    queue.append(nb)

    return infected_node_num
