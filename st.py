from copy import copy

class Node(object):
    def __init__(self, name=None):
        self.name = name
        self.labels = {}
        self.adiacent = []#id
    def __getitem__(self, key):
        try:
            return self.labels[key]
        except KeyError:
            return None

    def __setitem__(self, key, value):
        self.labels[key] = value

    def __hasitem__(self, key):
        return key in self.labels
    def id(self):
        if self.name:
            return self.name
        return hash(self)
    def __str__(self):
        if self.name:
            return 'Nodo %s' % self.name
        return 'Nodo anonimo: %x' % hash(self)

class Edge(object):
    def __init__(self, n1, n2):
        self.edge = (n1, n2)
        self.labels = {}
    def direct_equals(self, n1, n2):
        return ((n1 == self.edge[0]) and (n2 == self.edge[1]))
    def equals(self, n1, n2):
        return self.direct_equals(n1, n2) or self.direct_equals(n2,n1)
    def tuple(self):
        return self.edge

    def __getitem__(self, key):
        try:
            return self.labels[key]
        except KeyError:
            return None
    def __setitem__(self, key, value):
        self.labels[key] = value
    def __hasitem__(self, key):
        return key in self.labels

class DiGraph(object):
    def __init__(self):
        self.nodes = {} #'id':node
        self.edges = [] #(node,node)
    def get_adiacents(self, n):
        return [self.nodes[x.id()] for x in n.adiacent]
    def get_incidents(self, n):
        return [x for x in self.nodes.values() if n in x.adiacent]
    def get_incident_edge(self, n):
        l = []
        for e in self.edges:
            if n == e.tuple()[1]:
                l.append(e)
        return l
    def get_adiacent_edge(self, n):
        l = []
        for e in self.edges:
            if n == e.tuple()[0]:
                l.append(e)
        return l
    def get_edge(self, n1, n2):
        for edge in self.edges:
            if edge.direct_equals(n1,n2):
                return edge
        return None
    def get_edge_by_id(self, id1, id2):
        n1 = self.get_node(id1)
        n2 = self.get_node(id2)
        return self.get_edge(n1, n2)
    def add_edge_by_id(self, id1, id2):
        n1 = self.get_node(id1)
        n2 = self.get_node(id2)
        return self.add_edge(n1, n2)
    def add_edge(self, n1, n2):
        new_edge =Edge(n1,n2)
        self.edges.append(new_edge)
        n1.adiacent.append(n2)
        return new_edge
    def get_node(self, id):
        return self.nodes[id]
    def add_node(self, node):
        self.nodes[node.id()] = node

    def st(self):
        def low(n):
            min = n['dfn']
            for x in [edge.tuple()[1] for edge in self.get_adiacent_edge(n) if not edge['back']]:
                low_x = x['low']
                if not low_x:
                    low_x = low(x)
                if low_x is None:
                    print 'error on LOW:', x
                if low_x < min:
                    min = x['low']
            for w in [edge.tuple()[1] for edge in self.get_adiacent_edge(n) if edge['back']]:
                if w['dfn'] < min:
                    min = w['dfn']
            n['low'] = min
            return min
        def path(v):
            self.s['path_mark'] = True
            self.t['path_mark'] = True
            self.get_edge_by_id(self.s.id(), self.t.id())['path_mark'] = True

            #Caso1: c'e' un arco di riporto non marcato {v,w}: viene marcato l'arco e ritornato vw
            for adiac in self.get_adiacent_edge(v):
                if adiac['back'] and not adiac['path_mark']:
                    print 'CASO 1'
                    return [v, adiac.tuple()[1]]

            #Caso 2: esiste un arco dell'albero non marcato (v,w)
            for adiac_edge in self.get_adiacent_edge(v):
                if not adiac['back'] and not adiac['path_mark']:
                    print 'CASO 2'
                    #TODO: how can we find that path?
                    return []
            #Caso 3:
            for adiac in self.get_incident_edge(v):
                if adiac['back'] and not adiac['path_mark']:
                    print 'CASO 3'
                    assert adiac.tuple()[0]['dfn'] > adiac.tuple()[1]['dfn']
                    #Risaliamo l'albero seguendo FATH
                    ret = []
                    wi = adiac.tuple()[1]
                    while wi and wi != v:
                        wi['path_mark'] = True
                        ret.insert(0, wi)
                        wi = wi['fath']
                    return ret

            return []

        low(self.s)
        print 'S', self.s, self.s['low'], 'L'
        print 'T', self.t, self.t['low'], 'L'
        for n in self.nodes.values():
            print n, n['low'], n['dfn']
        #Its just a test, the real algo is a bit more complex
        print path(self.t)

    def print_graph(self):
        for v in self.nodes.values():
            print v, [str(ad) for ad in self.get_adiacents(v)]

class Graph(DiGraph):
    def __init__(self):
        DiGraph.__init__(self)
    def get_adiacents(self, n):
        return set(DiGraph.get_adiacents(self, n) + self.get_incidents(n))
    def get_adiacent_edge(self, n):
        l = []
        for e in self.edges:
            if n in e.tuple():
                l.append(e)
        return l
    def get_edge(self, n1, n2):
        for e in self.edges:
            if e.equals(n1, n2):
                return e
            else:
                print [str(x) for x in e.tuple()], 'is different from', n1, n2
        return None
    def st_graph(self, s, t):
        '''return a DiTree that is an st-graph'''
        assert s in self.nodes.values()
        assert t in self.nodes.values()
        assert s!=t
        assert self.get_edge(s,t) is not None
        print 'S =', s
        print 'T =', t
        dg = DiGraph()
        queue = [(None, s)]
        #s['auxvis'] = True
        count = 1
        while queue:
            fath, n_old= queue.pop()
            if n_old['auxvis']:
                continue
            n = Node(n_old.id())
            if n_old == s:
                dg.s = n
            if n_old == t:
                dg.t = n
            print n, [(str(v), v['auxvis']) for v in self.get_adiacents(n_old)]
            dg.add_node(n)
            if fath:
                print 'FATH', fath, n
                dg.add_edge(fath, n)
            n['dfn'] = count #Depth-First Numbering
            n['fath'] = fath
            n['auxvis'] = True
            n_old['auxvis'] = True
            n.adiacent = []
            for c in self.get_adiacents(n_old):
                if c['auxvis'] and fath.id() != c.id(): #Already visited
                    print 'Indietro:', n, c, '(father was:', fath, ')'
                    new_edge = dg.add_edge_by_id(n.id(), c.id()) #Arco all'indietro!!
                    new_edge['back'] = True
            new = [(n, c) for c in self.get_adiacents(n_old) if (not c['auxvis'])]
            new.reverse()
            queue += new
            count += 1

        if not dg.get_edge(dg.s, dg.t):
            aux = dg.s
            dg.s = dg.t
            dg.t = aux
        dg.print_graph()
        assert dg.get_edge(dg.s, dg.t) is not None
        return dg

    def st(self):
        def path(v):
            #Caso1: c'e' un arco di riporto non marcato {v,w}: viene marcato l'arco e ritornato vw
            if True in [adiac['vis'] for adiac in v.adiacent]:
                print 'CASO 1'
                for adiac in v.adiacent:
                    if adiac['vis']:
                        print "Path(%s) E' %s" % (str(v), str(adiac))
                        return[v, adiac]

            #Caso 2: esiste un arco dell'albero non marcato (v,w)
            if True in [adiac_edge['vis'] for adiac_edge in self.get_adiacent_edge(v)]:
                print 'CASO 2'
                return []
            return []



        random_edge = self.edges[0]
        self.s = random_edge.tuple()[0]
        self.t = random_edge.tuple()[1]
        stgraph = self.st_graph(self.s, self.t) #its a directed graph
        return stgraph.st()
        low(self.s)
        print 'S = ', self.s
        print 'T = ', self.t
        self.t['dfs'] = 1
        self.t['low'] = 1
    
        queue = [self.t, self.s]
        self.s['vis'] = True
        self.t['vis'] = True
        self.get_edge(self.s, self.t)['vis'] = True
        cont = 1
        v = queue.pop() #s
        while v != self.t:
            if not path(v):
                v['stn'] = cont
                print '%s ha stn = %d' % (str(v), v['stn'])
                cont += 1
            else:
                queue += path(v).reverse()
            v = queue.pop()

        self.t['stn'] = cont

def build_graph():
    a = Node('a')
    b = Node('b')
    c = Node('c')
    d = Node('d')
    e = Node('e')
    f = Node('f')
    g = Graph()
    g.add_node(a)
    g.add_node(b)
    g.add_node(c)
    g.add_node(d)
    g.add_node(e)
    g.add_node(f)
    g.add_edge(a, c)
    g.add_edge(a, b)
    g.add_edge(a, d)
    g.add_edge(b, c)
    g.add_edge(b, d)
    g.add_edge(c, d)
    g.add_edge(c, f)
    g.add_edge(c, e)
    g.add_edge(f, e)
    g.add_edge(d, f)

    return g

def build_graph2():
    s = Node('s')
    t = Node('t')
    a = Node('a')
    b = Node('b')
    c = Node('c')
    g = Graph()
    g.add_node(s)
    g.add_node(t)
    g.add_node(a)
    g.add_node(b)
    g.add_node(c)
    g.add_edge(s, t)
    g.add_edge(s, a)
    g.add_edge(s, b)
    g.add_edge(s, c)
    g.add_edge(a, b)
    g.add_edge(c, b)
    g.add_edge(t, b)
    g.add_edge(t, c)

    return g

if __name__ == '__main__':
    '''run a test'''
    g = build_graph() #the one on the book ;)
    g.print_graph() #useful for debug
    g.st()

