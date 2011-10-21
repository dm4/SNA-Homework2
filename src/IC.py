#!/usr/bin/env python

import random
import networkx as nx
from collections import deque

def bfs(G, queue, infected_node_num):
    while len(queue) > 0:
        node = queue.popleft()
        for nb in G.successors(node):
            if G.node[nb]['infected']:
                continue
            else:
                # check should be infected
                r = random.random()
                if r < 0.8:
                    G.node[nb]['infected'] = True
                    infected_node_num += 1
                    queue.append(nb)

    return infected_node_num
