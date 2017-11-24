from collections import defaultdict
import numpy as np;

# Helper Class, I have found at one of stackoverflow answer
class Graph(object):
    """ Graph data structure, undirected by default. """

    def __init__(self, connections, directed=False):
        self._graph = defaultdict(set)
        self._directed = directed
        self.add_connections(connections)

    def add_connections(self, connections):
        """ Add connections (list of tuple pairs) to graph """

        for node1, node2 in connections:
            self.add(node1, node2)

    def add(self, node1, node2):
        """ Add connection between node1 and node2 """

        self._graph[node1].add(node2)
        if not self._directed:
            self._graph[node2].add(node1)

    def remove(self, node):
        """ Remove all references to node """

        for n, cxns in self._graph.iteritems():
            try:
                cxns.remove(node)
            except KeyError:
                pass
        try:
            del self._graph[node]
        except KeyError:
            pass

    def is_connected(self, node1, node2):
        """ Is node1 directly connected to node2 """

        return node1 in self._graph and node2 in self._graph[node1]

    def find_path(self, node1, node2, path=[]):
        """ Find any path between node1 and node2 (may not be shortest) """

        path = path + [node1]
        if node1 == node2:
            return path
        if node1 not in self._graph:
            return None
        for node in self._graph[node1]:
            if node not in path:
                new_path = self.find_path(node, node2, path)
                if new_path:
                    return new_path
        return None

    def __str__(self):
        return '{}({})'.format(self.__class__.__name__, dict(self._graph))
    
nodes = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']
connections = [('A', 'B'), ('A', 'F'), ('C', 'B'),('C', 'E'), ('C', 'G'), ('D', 'C'), ('E', 'K'), ('E', 'H'), ('F', 'E'), ('G', 'J'), ('G', 'E'), ('H', 'F'), ('I', 'G'), ('J', 'I'), ('K', 'E')]
g = Graph(connections, directed=True)

adjancy = np.zeros((len(nodes), len(nodes)))

for c in nodes:
    for r in nodes:
        adjancy[nodes.index(c),nodes.index(r)] = 1 if(g.is_connected(r, c)) else 0
        
print(adjancy)
print("")

def hop(inp, matrix):
    result = np.zeros_like(matrix)
    for c in range(0, len(matrix)):
        for r in range(0, len(matrix[c])):
            if inp[c, r] == 1:
                left_exts = [matrix[r, a] for a in range(0, len(nodes))]
                for left_e in range(len(left_exts)):
                    result[c, left_e] = result[c, left_e] + left_exts[left_e]
                    result[c, left_e] = (1 if (result[c, left_e] >= 1) else 0)
                right_exts = [matrix[a, c] for a in range(0, len(nodes))]
                for right_e in range(len(right_exts)):
                    result[right_e, r] = result[right_e, r] + right_exts[right_e]
                    result[right_e, r] = (1 if(result[right_e, r] >= 1) else 0)
    return result
                    
print(hop(hop(adjancy, adjancy), adjancy))



##########################################################



G = np.array(adjancy)
print("G")
print(G)
print("")

glo = np.copy(adjancy)
item = G
for i in range(100):
    item = np.dot(item, G)
    item = (item >= 1) * 1.0
    glo += item
    glo = (glo >= 1) * 1.0
print("G * G * G")
print(glo)
print("")

glo = np.copy(adjancy)
hist = [0]*100
hist[0] = G
for i in range(2,100):
    item = np.dot(hist[i/2 - 1], hist[i/2 - 1])
    item = (item >= 1) * 1.0
    if i%2==1:
        item = np.dot(item, G)
    item = (item >= 1) * 1.0
    hist[i] = item
    glo += item
    glo = (glo >= 1) * 1.0
print("G4 = G2 * G2")
print(glo)
print("")

def warshall(a):
    n = len(a)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                a[i][j] = a[i][j] or (a[i][k] and a[k][j])
    return a

print("Warshall")
cl = warshall(G)
cl = (cl >= 1) * 1
print(cl * 1.0)



#############################################################################


import numpy as np
import matplotlib.pyplot as plt
import random
def rand_walk(mat, step_count):
    probs = [0] * len(nodes)
    cur = random.randint(0, len(nodes)-1)
    for j in range(0, step_count):
        if max(mat[cur]) < 1:
            probs[cur] += 1
            cur = random.randint(0, len(nodes)-1)
            continue
        for i in range(len(nodes)-1):
            if mat[cur][i] == 1:
                probs[cur] += 1
                cur = i
                break
    probs = np.array(probs)
    return probs / float(np.sum(probs))

print rand_walk(adjancy, 10000)

def rand_walk_impr(mat, step_count):
    probs = [0] * len(nodes)
    cur = random.randint(0, len(nodes)-1)
    for j in range(0, step_count):
        num = random.randint(1, 100)
        if (num > 20):
            if max(mat[cur]) < 1:
                probs[cur] += 1
                cur = random.randint(0, len(nodes)-1)
                continue
            for i in range(len(nodes)-1):
                if mat[cur][i] == 1:
                    probs[cur] += 1
                    cur = i
                    break
        else:
            cur = random.randint(0, len(nodes)-1)
    probs = np.array(probs)
    return probs / float(np.sum(probs))

print rand_walk_impr(adjancy, 10000)