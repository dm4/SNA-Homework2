#!/usr/bin/env python

import random
import networkx as nx
from collections import deque

def bfs(G, queue, infected_node_num):
    prob = 0.95
    while len(queue) > 0:
        prob -= 0.0001
        node = queue.popleft()
        for nb in G.successors(node):
            if G.node[nb]['infected'] or G.node[nb]['blocked']:
                continue
            else:
                # check should be infected
                r = random.random()
                if r < prob:
                    G.node[nb]['infected'] = True
                    infected_node_num += 1
                    queue.append(nb)

    return infected_node_num
