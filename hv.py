import random

class GNode(object):
	_id = 0
	def __init__(self):
		self.id = self.__class__._id
		self.__class__._id += 1
		self.dx = 0
		self.dy = 0
		self.parent = None #It's root
		self.childs = [None, None]
		self.size = 1
		self.extra = None

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
		print '%02d' % self.id, self.dx, self.dy
		if self.childs[0]:
			print ' '*(indent+0),
			print 'left:'
			self.childs[0].print_tree(indent+4)
		if self.childs[1]:
			print ' '*(indent+0),
			print 'right:'
			self.childs[1].print_tree(indent+4)
		
def ahnentafel_to_tree(enc_tree, start=0):
	if len(enc_tree) <= start:
		return None
	char = enc_tree[start]
	if char == '0':
		return None
	node = GNode()
	left_child = ahnentafel_to_tree(enc_tree, 2*start+1)
	if left_child:
		node.set_left_child(left_child)
	right_child = ahnentafel_to_tree(enc_tree, 2*start+2)
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
		return 1
	h0 = hv(g.childs[0]) #valid even with no childs
	h1 = hv(g.childs[1])
	if (not g.childs[1]) or (g.childs[0] and g.childs[0].size > g.childs[1].size):
		g.childs[0].dx = 1
		g.childs[0].dy = 0
		if g.childs[1]:
			g.childs[1].dx = 0
			g.childs[1].dy = h0 #+ 1
	else:
		g.childs[1].dx = 1
		g.childs[1].dy = 0
		if g.childs[0]:
			g.childs[0].dx = 0
			g.childs[0].dy = h1#+1
	return h0+h1
	
if __name__ == '__main__':
	#t = ahnentafel_to_tree('1111011')
	t = ahnentafel_to_tree('1111111')
	hv(t)
	t.print_tree()

