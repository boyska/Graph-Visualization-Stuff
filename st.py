from debugger import debug, info, warning
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

    def __str__(self):
        return 'Edge: %s->%s' % (self.edge[0],self.edge[1])
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
            if n['low']:
                return n['low']
            min = n['dfn']
            for x in [edge.tuple()[1] for edge in self.get_adiacent_edge(n) if not edge['back']]:
                low_x = x['low']
                if not low_x:
                    low_x = low(x)
                if low_x is None:
                    warning('error on LOW:' + str(x))
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
            self.get_edge_by_id(self.t.id(), self.s.id())['path_mark'] = True

            #Caso1: c'e' un arco di riporto non marcato {v,w}: viene marcato l'arco e ritornato vw
            for adiac in self.get_adiacent_edge(v):
                if adiac['back'] and not adiac['path_mark']:
                    debug('CASO 1: arco di riporto non marcato (v,w)')
                    adiac['path_mark'] = True
                    return [v, adiac.tuple()[1]]

            #Caso 2: esiste un arco dell'albero non marcato (v,w)
            for adiac_edge in self.get_adiacent_edge(v):
                if (not adiac['back']) and (not adiac['path_mark']):
                    debug('CASO 2: arco dell albero non marcato')
                    #TODO: check if it works
                    ret = [v]
                    w = wi = adiac.tuple()[1]
                    adiac['path_mark'] = True
                    while True:
                        debug(str(wi) + 'ret now' + str([str(n) for n in ret]))
                        wi['path_mark'] = True
                        ret.append( wi)
                        for backedge in self.get_adiacent_edge(wi):
                            if not backedge['back']:
                                continue
                            u = backedge.tuple()[1]
                            #mah...
#                            if u['dfn'] != w['low']:
#                                continue
                            u_v = self.get_edge(u, v)
                            if u_v and not u_v['back']:
                                u['path_mark'] = True
                                u_v['path_mark'] = True
                                ret.append(u)
                                return ret
                        for treeedge in self.get_adiacent_edge(wi):
                            if backedge['back']:
                                continue
                            if backedge.tuple()[1]['low'] == w['low']:
                                wi = backedge.tuple()[1]
                                wi['path_mark'] = True
                                backedge['path_mark'] = True
                                break
                        else: #Nothing found
                            raise Exception('Where do we go now?')

            #Caso 3: Esiste un arco di riporto non marcato
            for adiac in self.get_incident_edge(v):
                if adiac['back'] and not adiac['path_mark']:
                    debug('CASO 3: Arco di riporto non marcato (w,v)')
                    assert adiac.tuple()[0]['dfn'] > adiac.tuple()[1]['dfn']
                    #Risaliamo l'albero seguendo FATH
                    ret = [v]
                    wi = adiac.tuple()[0]
                    adiac['path_mark'] = True
                    while wi != v:
                        wi['path_mark'] = True
                        adiac['path_mark'] = True
                        ret.append(wi)
                        wi = wi['fath']
                    return ret
            #Caso 4: tutti gli archi incidenti a v sono marcati
            if False not in [adiac['path_mark'] for adiac in self.get_incident_edge(v)]:
                debug('Caso 4: tutti gli archi incidenti a v sono marcati')
                return []

            raise Exception('Per %s Nessun caso va bene!!' % str(v))

        for v in self.nodes.values():
            low(v)
        #Its just a test, the real algo is a bit more complex
        stack = [self.t, self.s]
        self.s['vis'] = True
        self.t['vis'] = True
        self.get_edge(self.t, self.s)['vis'] = True
        cont = 1
        v = stack.pop() #s
        while v != self.t:
            res = path(v)
            debug('path(%s) = %s' % (str(v), [str(e) for e in res]))
            if res == [] and not v['stn']:
                v['stn'] = cont
                cont += 1
            else:
                res.reverse()
                stack.extend(res[1:])
            v = stack.pop()

        self.t['stn'] = cont
        for n in self.nodes.values():
            debug('%s has STN: %d' % (str(n), n['stn']))
    def print_graph(self):
        for v in self.nodes.values():
            print v, [str(ad) for ad in self.get_adiacents(v)]
    def print_more(self):
        for v in self.nodes.values():
            print '%s:' % str(v),
            for e in self.get_adiacent_edge(v):
                print e.tuple()[1], '(',
                for key,value in e.labels.items():
                    print '%s=%s' % (key,value),
                print '),',
            print


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
        return None
    def st_graph(self, s):
        '''return a DiTree that is an st-graph'''
        assert s in self.nodes.values()
        dg = DiGraph()
        queue = [(None, s)]
        #s['auxvis'] = True
        count = 1
        while queue:
            fath, n_old= queue.pop()
            if n_old['auxvis']:
                continue
            n = Node(n_old.id())
            print n, [(str(v), v['auxvis']) for v in self.get_adiacents(n_old)]
            dg.add_node(n)
            if fath:
                debug('FATH %s %s' % (str(fath), str(n)))
                dg.add_edge(fath, n)
            n['dfn'] = count #Depth-First Numbering
            n['fath'] = fath
            n['auxvis'] = True
            n_old['auxvis'] = True
            n.adiacent = []
            for c in self.get_adiacents(n_old):
                if c['auxvis'] and fath.id() != c.id(): #Already visited
                    new_edge = dg.add_edge_by_id(n.id(), c.id()) #Arco all'indietro!!
                    new_edge['back'] = True
            new = [(n, c) for c in self.get_adiacents(n_old) if (not c['auxvis'])]
            new.reverse()
            queue += new
            count += 1

        s_t = [e for e in dg.get_adiacent_edge(dg.get_node(s.id())) if not e['back']][0]
        dg.t = dg.get_node(s.id())
        dg.s = s_t.tuple()[1]
        dg.print_more()
        assert dg.get_edge(dg.t, dg.s) is not None
        print 'S', dg.s, 'T', dg.t
        return dg

    def st(self):
        random_edge = self.edges[0]
        self.s = random_edge.tuple()[0]
        self.t = random_edge.tuple()[1]
        stgraph = self.st_graph(self.s) #its a directed graph
        stgraph.st()
        return stgraph
        low(self.s)
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
                info( '%s ha stn = %d' % (str(v), v['stn']))
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

def test1():
    g = build_graph() #the one on the book ;)
    g.print_graph() #useful for debug
    st = g.st()
    #S has the minimum value
    assert st.s['stn'] == 1
    #T has the maximum value
    for n in st.nodes.values():
        if n != st.t:
            assert n['stn'] < st.t['stn']
    #It is a valid ST-numbering
    for n in st.nodes.values():
        for e in st.edges:
            if e['back']:
                continue
            u = e.tuple()[0]
            v = e.tuple()[1]
            if u['stn'] >= v['stn']:
                warning('%s:%d -> %s:%d' % (str(u), u['stn'], str(v), v['stn']))
            assert u['stn'] < v['stn']
    info('The ST-numbering has been properly computed')

if __name__ == '__main__':
    '''run a test'''
    test1()

