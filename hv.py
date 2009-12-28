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

def random_tree(len):
    l = ['1']
    for i in range(len):
        l.append(str(random.randint(0,1)))
    return ''.join(l)
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

