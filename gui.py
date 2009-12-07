import sys
import random

from PyQt4 import QtGui, QtCore, Qt

import hv

class GraphScene(QtGui.QGraphicsScene):
    def __init__(self):
        QtGui.QGraphicsScene.__init__(self)
        self.points = {} #id:item
        self.lines = {}
    
    def from_gnode(self, t):
        self._gnode_to_point(t)
    def _gnode_to_point(self, n):
        if not n:
            return
        if n.parent:
            parent_point = self.points[n.parent.id]
            parent_coord = parent_point.rect().topLeft()
        else:
            parent_coord = QtCore.QPointF(0,0)

        self.points[n.id] = QtGui.QGraphicsEllipseItem(
                parent_coord.x()+15*n.dx, parent_coord.y()+15*n.dy, 5, 5)
        self.points[n.id].setBrush(QtGui.QColor('red'))
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
        self.connect(self.random, QtCore.SIGNAL('clicked()'), self.on_random)

        self.main_vbox.addWidget(self.view)
        self.main_vbox.addLayout(self.input_hbox)

        widg = QtGui.QWidget()
        self.setCentralWidget(widg)
        self.centralWidget().setLayout(self.main_vbox)

    
    def on_ok(self):
        print 'ok'
        scene = GraphScene()
        tree = hv.ahnentafel_to_tree(str(self.input.text()))
        hv.hv(tree)
        scene.from_gnode(tree)
        self.view.setScene(scene)
        self.view.resetCachedContent()
    
    def on_random(self):
        ahnentafel_enc = hv.random_tree(random.randint(5, 15))
        self.input.setText(ahnentafel_enc)
        self.on_ok()



if __name__ == '__main__':
    App = QtGui.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(App.exec_())
