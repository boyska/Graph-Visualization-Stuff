from debugger import debug, info, warning
from copy import copy
import random

import col_choose

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
    def to_Graph(self):
        g = Graph()
        g.nodes = self.nodes
        g.edges = self.edges
        return g

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

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __add__(self, point):
        if not isinstance(point, Point):
            try:
                point = Point(*point)
            except:
                raise TypeError('%s is not a valid Point' % str(point))
        new = copy(self)
        new.x += point.x
        new.y += point.y
        print self, '+', point, '=', new
        return new
    def __eq__(self, point2):
        return type(point2) is Point and self.x == point2.x and self.y == point2.y
    def __str__(self):
        return '(%d,%d)' % (self.x, self.y)
    def __repr__(self):
        return 'Point %s' % str(self)

class Line(object):
    def __init__(self, start, end):
        if type(start) is Point:
            self.start = start
        else:
            self.start = Point(*start)
        if type(end) is Point:
            self.end = end
        else:
            self.end = Point(*end)
        if self.is_point():
            warning('%s:This line is a point!' % str(self))
    def __str__(self):
        return 'L[%s - %s]' % (str(self.start), str(self.end))
    def is_point(self):
        return self.start == self.end
    def is_horizontal(self):
        return self.start.y == self.end.y
    def is_vertical(self):
        return self.start.x == self.end.x
    def is_straight(self):
        return self.is_vertical() or self.is_horizontal()

class Polyline(object):
    def __init__(self):
        self.lines = []
    def add_line(self, line):
        if self.lines and not self.lines[-1].end == line.start:
            raise ValueError('New line start at %s, but the previous end at %s' %\
                    (str(line.start), str(self.lines[-1].end)))
        if not line.is_straight():
            raise ValueError('Line %s is not straight!')
        if self.lines:
            last = self.lines[-1]
            if last.is_horizontal() and line.is_horizontal() \
                    and not last.is_point() and not line.is_point():
                raise ValueError('You cant concatenate two horizontal lines! %s-%s' %\
                        (str(last), str(line)))
            if last.is_vertical() and line.is_vertical() \
                    and not last.is_point() and not line.is_point():
                raise ValueError('You cant concatenate two vertical lines! %s-%s' %\
                        (str(last), str(line)))
        self.lines.append(line)
    def __str__(self):
        segments = []

        if self.lines[0].is_horizontal():
            segments.append('H(%d)%d:%d' % (self.lines[0].start.y, self.lines[0].start.x, self.lines[0].end.x))
        else:
            segments.append('V(%d)%d:%d' % (self.lines[0].start.x, self.lines[0].start.y, self.lines[0].end.y))

        for l in self.lines[1:]:
            if l.is_horizontal():
                segments.append('H%d:%d' % (l.start.x, l.end.x))
            else:
                segments.append('V%d:%d' % (l.start.y, l.end.y))

        return 'PL:[%s]' % ', '.join(segments)
    @staticmethod
    def hv(start, end):
        pl = Polyline()
        if start.x == end.x or start.y == end.y:
            pl.add_line(Line(start, end))
            return pl
        pl.add_line(Line(start, (end.x, start.y)))
        pl.add_line(Line((end.x, start.y), end))
        return pl
    @staticmethod
    def vh(start, end):
        pl = Polyline()
        if start.x == end.x or start.y == end.y:
            pl.add_line(Line(start, end))
            return pl
        pl.add_line(Line(start, (start.x, end.y)))
        pl.add_line(Line((start.x, end.y), end))
        return pl
    @staticmethod
    def hvh(start, end, passing_col):
        pl = Polyline()
        pl.add_line(Line(start, (passing_col, start.y)))
        pl.add_line(Line((passing_col, start.y), (passing_col, end.y)))
        pl.add_line(Line((passing_col, end.y), end))
        return pl

class Drawing(object):
    def __init__(self, graph):
        self.graph = graph.to_Graph()
        self.positions = {} #Node.id():Point
        self.lines = [] #Polyline()
    def draw(self):
        g = self.graph
        allocated_col = [] #int TODO: do we really need it?
        pending_edges = {} #node_from.id():[col1, col2]
        avail_sides = {}
        nodes = g.nodes.values()

        # Initialize avail_sides
        for n in nodes:
            #-1 is left, 0 is down, 1 is right, 2 is up
            avail_sides[n.id()] = [-1, 0, 1, 2]

        #### Routine definitions
        def get_position(node):
            return self.positions[node.id()]
        def set_position(node, column, line):
            '''Put a node somewhere'''
            self.positions[node.id()] = Point(column, line)
            return self.positions[node.id()]
        def allocate_column(node, column=None):
            #If none, uses himself column
            if column is None:
                column = get_position(node).x
            allocated_col.append(column)
            if node.id() in pending_edges:
                pending_edges[node.id()].append(column)
            else:
                pending_edges[node.id()] = [column]
        allocate_column.leftish_col = 0
        allocate_column.rightish_col = 3
        def allocate_column_left(node):
            allocate_column.leftish_col -= 1
            allocate_column(node, allocate_column.leftish_col)
        def allocate_column_right(node):
            allocate_column.rightish_col += 1
            allocate_column(node, allocate_column.rightish_col)

        def stn(node):
            return node['stn']
        def connect_points(a, b, col):
            if avail_sides[b.id()] == [2]: #Last, 4-degree node
                pl = Polyline.hvh(get_position(a), get_position(b)+(0,1), col)
                pl.add_line(Line(get_position(b)+(0,1), get_position(b)))
            else:
                pl = Polyline.hvh(get_position(a), get_position(b), col)
                if get_position(b).x < col:
                    avail_sides[b.id()].remove(1)
                elif get_position(b).x == col:
                    avail_sides[b.id()].remove(0)
                else:
                    avail_sides[b.id()].remove(-1)

            self.lines.append(pl)
            if get_position(a).x < col:
                avail_sides[a.id()].remove(1)
            elif get_position(a).x == col:
                avail_sides[a.id()].remove(2)
            else:
                avail_sides[a.id()].remove(-1)

            pending_edges[a.id()].remove(col)

            return pl

        ### End routine definition

        #Sorting by ST-Numbering is the way!
        nodes.sort(key=stn)
        debug(str([(n.id(), n['stn']) for n in  nodes]))

        #Draw 1, 2 and the edge between them
        v1 = nodes.pop(0)
        v2 = nodes.pop(0)
        set_position(v1, 0, 0) #The center of drawing is v1
        set_position(v2, 3, 0)
        v1_v2_line = Polyline()
        v1_v2_line.add_line(Line((0,0), (0, -1)))
        v1_v2_line.add_line(Line((0,-1), (3, -1)))
        v1_v2_line.add_line(Line((3,-1), (3, 0)))
        self.lines.append(v1_v2_line)
        #So ugly
        pending_edges[v1.id()] = []
        pending_edges[v2.id()] = []
        allocate_column(v1)
        if len(g.get_adiacents(v1)) > 2:
            allocate_column(v1, 1)
        if len(g.get_adiacents(v1)) > 3:
            allocate_column_left(v1)
        allocate_column(v2)
        if len(g.get_adiacents(v2)) > 2:
            allocate_column(v2, 2)
        if len(g.get_adiacents(v2)) > 3:
            allocate_column_right(v2)

        line = 1
        v = nodes.pop(0)
        while len(nodes) >= 0:
            print 'now on', v
            print pending_edges
            #Choose column
            available_cols = []
            for x in g.get_adiacents(v):
                if x.id() in pending_edges:
                    for edge in pending_edges[x.id()]:
                        available_cols.append((edge, x.id()))
            if not available_cols:
                raise Exception('sth went wrong: no available columns!')
            #col is the chosen column
            degree = len([x for x in g.get_adiacents(v) if x['stn'] < v['stn']])
#            if degree == 1:
#                col = available_cols[0][0]
#                chosen_col = [available_cols[0]]
#                set_position(v, col, line)
#            else:
            debug('Choosing col for %s from %s' % (v.id(), str(available_cols)))
            col = available_cols[len(available_cols)/2]
            chosen_col = col_choose.column_choose(available_cols)
            #print available_cols, '=>', chosen_col
            col = chosen_col[(len(chosen_col)-1)/2][0]
            set_position(v, col, line)
            debug('Chosen: %d' % col)
            for column in chosen_col:
                debug('Connect %s to %s through %d' % (column[1], v.id(), column[0]))
                connect_points(g.nodes[column[1]], v, column[0])

            out_degree = len(g.get_adiacents(v)) - 4 + len(avail_sides[v.id()])
            print avail_sides[v.id()]
            debug('%s has %d out_degree' % (v.id(), out_degree))
            allocate_column(v)
            if out_degree > 1:
                if -1 in avail_sides[v.id()]:
                    allocate_column_left(v)
                    if out_degree > 2:
                        assert 1 in avail_sides[v.id()]
                        allocate_column_right(v)
                else:
                    assert out_degree == 2
                    allocate_column_right(v)

            line += 1
            try:
                v = nodes.pop(0)
            except:
                break
        #TODO: last node
        #We could have 4 incoming edges!
        


        print self.positions
        

def build_graph1():
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

def build_graph_k4():
    a = Node('a')
    b = Node('b')
    c = Node('c')
    d = Node('d')
    g = Graph()
    g.add_node(a)
    g.add_node(b)
    g.add_node(c)
    g.add_node(d)
    g.add_edge(a, b)
    g.add_edge(a, c)
    g.add_edge(a, d)
    g.add_edge(b, a)
    g.add_edge(b, d)
    g.add_edge(b, c)
    g.add_edge(c, a)
    g.add_edge(c, b)
    g.add_edge(c, d)
    g.add_edge(d, a)
    g.add_edge(d, b)
    g.add_edge(d, c)

    return g

def build_graph_k5():
    a = Node('a')
    b = Node('b')
    c = Node('c')
    d = Node('d')
    e = Node('e')
    g = Graph()
    g.add_node(a)
    g.add_node(b)
    g.add_node(c)
    g.add_node(d)
    g.add_node(e)
    g.add_edge(a, b)
    g.add_edge(a, c)
    g.add_edge(a, d)
    g.add_edge(a, e)
    g.add_edge(b, a)
    g.add_edge(b, c)
    g.add_edge(b, d)
    g.add_edge(b, e)
    g.add_edge(c, a)
    g.add_edge(c, b)
    g.add_edge(c, d)
    g.add_edge(c, e)
    g.add_edge(d, a)
    g.add_edge(d, b)
    g.add_edge(d, c)
    g.add_edge(d, e)

    return g

def build_graph_cycle(n=6):
    g = Graph()
    first = None
    prev = None
    for i in range(n):
        node = Node(chr(ord('a')+i))
        g.add_node(node)
        if prev:
            g.add_edge(prev, node)
        else:
            first = node
        prev = node
    g.add_edge(node, first)
    return g



def build_graph_random(n=6):
    g = build_graph_cycle(n)
    for a in g.nodes.values():
        for b in g.nodes.values():
            if a == b:
                continue
            if len(g.get_adiacents(a)) == 4 or len(g.get_adiacents(b)) ==4:
                continue
            if random.randint(0,1):
                g.add_edge(a,b)

    return g

def stn_check(st):
    #S has the minimum value
    assert st.s['stn'] == 1
    #T has the maximum value
    for n in st.nodes.values():
        if n != st.t:
            assert n['stn'] < st.t['stn']
    #TODO: complete st-numbering check
    info('The ST-numbering has been properly computed')

if __name__ == '__main__':
    '''run a test'''
    dg = build_graph_k5().st()
    stn_check(dg)
    draw = Drawing(dg)
    draw.draw()

