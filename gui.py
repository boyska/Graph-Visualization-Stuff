import sys
import random

from PyQt4 import QtGui, QtCore, Qt

import hv

class GraphScene(QtGui.QGraphicsScene):
    def __init__(self):
        QtGui.QGraphicsScene.__init__(self)
        self.points = {} #id:item
        self.lines = {}
        self.labels = {}
    
    def from_gnode(self, t):
        self._gnode_to_point(t)
    def _gnode_to_point(self, n):
        SCALE=35
        CIRCLE_SIZE=10
        if not n:
            return
        print 'drawing', n,
        if n.parent:
            parent_point = self.points[n.parent.id]
            parent_coord = parent_point.rect().topLeft()
        else:
            parent_coord = QtCore.QPointF(0,0)
        print '@ (%d,%d)' % (parent_coord.x()+SCALE*n.dx, parent_coord.y()+SCALE*n.dy)

        self.points[n.id] = QtGui.QGraphicsEllipseItem(
                parent_coord.x()+SCALE*n.dx, parent_coord.y()+SCALE*n.dy, CIRCLE_SIZE, CIRCLE_SIZE)
        self.points[n.id].setBrush(QtGui.QColor('red'))
        self.points[n.id].setToolTip(n.label)
        self.points[n.id].setZValue(1) #they're on top of lines

        self.labels[n.id] = QtGui.QGraphicsTextItem(n.label)
        self.labels[n.id].setPos(
                parent_coord.x()+SCALE*n.dx + CIRCLE_SIZE, parent_coord.y()+SCALE*n.dy)
        self.labels[n.id].setZValue(2) #they're on top of everythin
        self.addItem(self.labels[n.id])
        self.addItem(self.points[n.id])

        if n.parent:
            self.lines[(n.id, n.parent.id)] = QtGui.QGraphicsLineItem(
                    parent_point.rect().center().x(), parent_point.rect().center().y(),
                    self.points[n.id].rect().center().x(), self.points[n.id].rect().center().y())
            self.addItem(self.lines[(n.id, n.parent.id)])

        self._gnode_to_point(n.childs[0])
        self._gnode_to_point(n.childs[1])

class Window(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.showMaximized()
        
        self.view = QtGui.QGraphicsView()
        self.main_vbox = QtGui.QVBoxLayout()
                
        self.input_hbox = QtGui.QHBoxLayout()
        self.input = QtGui.QLineEdit()
        self.input_hbox.addWidget(self.input)
        self.ok = QtGui.QPushButton('OK')
        self.input_hbox.addWidget(self.ok)
        self.connect(self.ok, QtCore.SIGNAL('clicked()'), self.on_ok)
        self.connect(self.input, QtCore.SIGNAL('editingFinished()'), self.on_ok)
        self.random = QtGui.QPushButton('random')
        self.input_hbox.addWidget(self.random)
        self.spin_box = QtGui.QSpinBox()
        self.spin_box.setMaximum(40)
        self.spin_box.setMinimum(1)
        self.input_hbox.addWidget(self.spin_box)
        self.complete = QtGui.QPushButton('complete')
        self.input_hbox.addWidget(self.complete)
        self.fib = QtGui.QPushButton('fib')
        self.input_hbox.addWidget(self.fib)
        self.connect(self.random, QtCore.SIGNAL('clicked()'), self.on_random)
        self.connect(self.complete, QtCore.SIGNAL('clicked()'), self.on_complete)
        self.connect(self.fib, QtCore.SIGNAL('clicked()'), self.on_fib)

        self.main_vbox.addWidget(self.view)
        self.main_vbox.addLayout(self.input_hbox)

        widg = QtGui.QWidget()
        self.setCentralWidget(widg)
        self.centralWidget().setLayout(self.main_vbox)

    
    def on_ok(self):
        print 'ok'
        scene = GraphScene()
        tree = hv.ahnentafel_to_tree(str(self.input.text()))
        with open('lastgraph.dot', 'w') as buf:
            buf.write('digraph G {\n%s}\n' % tree.to_graphviz())
        hv.hv(tree)
        scene.from_gnode(tree)
        self.view.setScene(scene)
        self.view.resetCachedContent()
    
    def on_fib(self):
        ahnentafel_enc = hv.fib_tree(self.spin_box.value())
        self.input.setText(ahnentafel_enc)
        self.on_ok()
    
    def on_complete(self):
        ahnentafel_enc = hv.complete_tree(self.spin_box.value())
        self.input.setText(ahnentafel_enc)
        self.on_ok()
    
    def on_random(self):
        ahnentafel_enc = hv.random_tree(self.spin_box.value())
        self.input.setText(ahnentafel_enc)
        self.on_ok()



if __name__ == '__main__':
    App = QtGui.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(App.exec_())
