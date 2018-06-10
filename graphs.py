

class MyGraph:

    def __init__(self, g={}):
        self.g = g


    def print_graph(self):
        [print (node, " --> " ,self.g[node]) for node in self.g.keys()]

    def get_nodes(self):
        return list(self.g.keys())

    def get_edges(self):
        return [(o, d) for o, nodes_dest in self.g.items() for d in nodes_dest]

    def add_node(self, node):
        if node not in self.g.keys():
            self.g[node]=[]

    def add_edge(self, orig, dest):
        if orig not in self.g.keys():
            self.add_node(orig)
        if dest not in self.g.keys():
            self.add_node(dest)
        if dest not in self.g[orig]:
            self.g[orig].append(dest)

    def get_successors(self, node):
        return list(self.g[node])

    def get_predecessors(self, node):
        return [node_orig for node_orig, nodes_dest in self.g.items() if node in nodes_dest]

    def get_adjacents(self, node):
        s = self.get_successors(node)
        p = self.get_predecessors(node)
        return list(set(s+p))

    def out_degree(self, node):
        return len(self.g[node])

    def in_degree(self, node):
        return len(self.get_predecessors(node))

    def degree(self, node):
        return len(self.get_adjacents(node))

    def reachableBFS (self, node):
        to_visit = [node]
        res=[]
        while to_visit:
            actual_node = to_visit.pop(0) #index required to remove the first element of the list
            if node!= actual_node : res.append(actual_node)
            to_visit.extend([elem for elem in self.g[actual_node] if elem not in res and elem not in to_visit])
        return res

    def reachableDFS (self, node):
        to_visit = [node]
        res = []
        while to_visit:
            actual_node = to_visit.pop(0)
            if node!= actual_node : res.append(actual_node)
            aux = [elem for elem in self.g[actual_node] if elem not in res and elem not in to_visit]
            to_visit = aux + to_visit
        return res


    def distance(self, orig, dest):    #distancia!! do caminho + curto
        if orig == dest: return 0
        l = [(orig, 0)]
        visited = [orig]
        while l:
            actual_node, dist = l.pop(0)
            for elem in self.g[actual_node]:
                if elem == dest:
                    return dist + 1    #nao acaba o for, por isso passa-se ao elif na mesma podendo ficar com mais do que uma distancia, se tiver mais do que um caminho????????
                elif elem not in visited:
                    l.append((elem, dist + 1))
                    visited.append(elem)
        return float("inf")


    def shortest_path(self, orig, dest):
        if orig == dest: return []
        l = [(orig, [])]
        visited = []
        while l:
            actual_node, path = l.pop(0)
            for elem in self.g[actual_node]:
                if elem == dest:
                    return [orig] + path + [elem]
                elif elem not in visited:
                    l.append((elem, path + [elem]))
                    visited.append(elem)
        return None


    def reachable_with_dist(self, node):
        res = []
        l = [(node, 0)]
        while len(l) > 0:
            actual_node, dist = l.pop(0)
            if actual_node != node: res.append((actual_node, dist))
            for elem in self.g[actual_node]:
                if elem not in [x[0] for x in l + res]:
                    l.append((elem, dist + 1))
        return res

    def node_has_cycle (self, node):
        l = [node]
        res = False
        visited = [node]
        while l:
            actual_node = l.pop()
            for elem in self.g[actual_node]:
                if elem == node: return True
                elif elem not in visited:
                    l.append(elem)
                    visited.append(elem)
        return res

    def has_cycle(self):
        for v in self.g.keys():
            if self.node_has_cycle(v): return True
        return False


    def size(self):
        return len(self.get_nodes()), len(self.get_edges)
    
    
  

def composition(k, seq):
    res = []
    for i in range(len(seq)-k+1):
        res.append(seq[i,i+k])
    res.sort()
    return res
    
   
##auxiliary functions
def suffix(seq):
    return seq[1:]

def prefix(seq):
    return seq[:1]   