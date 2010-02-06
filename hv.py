import random

class GNode(object):
    _id = 0
    def __init__(self, label=None):
        self.id = self.__class__._id
        if label is not None:
            self.label = label
        else:
            self.label = '%d' % self.id
        self.__class__._id += 1
        self.dx = 0
        self.dy = 0
        self.parent = None #It's root
        self.childs = [None, None]
        self.size = 1
        self.extra = None

    def __str__(self):
        return 'Gnode %s' % self.label
    def set_right_child(self, child):
        self.childs[1] = child
        self.childs[1].parent = self
        self.incr_size(child.size)
    def set_left_child(self, child):
        self.childs[0] = child
        self.childs[0].parent = self
        self.incr_size(child.size)

    def incr_size(self, size):
        self.size += size
        if self.parent:
            self.parent.incr_size(size)

    def print_tree(self, indent=1):
        print ' '*indent,
        print '%s' % self.label, self.dx, self.dy
        if self.childs[0]:
            print ' '*(indent+0),
            print 'left:'
            self.childs[0].print_tree(indent+4)
        if self.childs[1]:
            print ' '*(indent+0),
            print 'right:'
            self.childs[1].print_tree(indent+4)
        
def ahnentafel_to_tree(enc_tree):
    if ',' in enc_tree:
        return ahnentafel_list_to_tree(enc_tree.split(','))
    return ahnentafel_list_to_tree(enc_tree)

def ahnentafel_list_to_tree(enc_tree, start=0):
    if len(enc_tree) <= start:
        return None
    char = enc_tree[start]
    if char == '0':
        return None
    node = GNode(char)
    left_child = ahnentafel_list_to_tree(enc_tree, 2*start+1)
    if left_child:
        node.set_left_child(left_child)
    right_child = ahnentafel_list_to_tree(enc_tree, 2*start+2)
    if right_child:
        node.set_right_child(right_child)
    return node

def fib_tree(h):
    l = ['0'] * (2**h-1)
    def fib_rec(l, start, subheigth):
        if subheigth <= 0:
            return
        l[start] = '1'
        fib_rec(l, 2*start+1, subheigth-1)
        fib_rec(l, 2*start+2, subheigth-2)
    fib_rec(l, 0, h)
    while l[-1] == '0':
        l.pop()

    return ''.join(l)
def fib_check(ahnentafel):
    raise NotImplementedError()
def complete_tree(h):
    l = []
    last = 'a'
    for i in range(2**h-1):
        l.append(last)
        if ord(last) < ord('z'):
            last = chr(1+ord(last))
        else:
            last = 'a'
    return ','.join(l)

def random_tree(len):
    last_char = 'a'
    l = ['a']
    for i in range(len):
        yes = random.randint(0,1)
        if yes:
            if ord(last_char)<= ord('z'):
                last_char = chr(1+ord(last_char))
            else:
                last_char = 'a'
            l.append(last_char)
        else:
            l.append('0')
    return ','.join(l)
def hv(g):
    if not g:
        return 0
    if g.childs == [None, None]:
        print g, 'has no childs'
        return 0
    h0 = hv(g.childs[0]) #valid even with no childs
    h1 = hv(g.childs[1])
    if (not g.childs[1]) or (g.childs[0] and g.childs[0].size > g.childs[1].size):
        print 'on', g, 'case 1', h1
        g.childs[0].dx = h1+1
        g.childs[0].dy = 0
        if g.childs[1]:
            g.childs[1].dx = 0
            g.childs[1].dy = 1 
    else:
        print 'on', g, 'case 2', h0
        g.childs[1].dx = h0+1
        g.childs[1].dy = 0
        if g.childs[0]:
            g.childs[0].dx = 0
            g.childs[0].dy = 1
    return h0+h1+1
    
if __name__ == '__main__':
    #t = ahnentafel_to_tree('1111011')
    t = ahnentafel_to_tree('a,b,c,d')
    hv(t)
    t.print_tree()

