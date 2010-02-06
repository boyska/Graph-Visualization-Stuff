import sys
import random
import time

from PyQt4 import QtGui, QtCore, Qt

import st
from debugger import debug

class GraphScene(QtGui.QGraphicsScene):
    def __init__(self):
        QtGui.QGraphicsScene.__init__(self)
    def from_drawing(self, draw):
        SCALE=35
        CIRCLE_SIZE=10
        colors = [QtCore.Qt.yellow, QtCore.Qt.red, QtCore.Qt.black,
                QtCore.Qt.blue, QtCore.Qt.green]
        i=0
        for poly in draw.lines:
            #draw line
            #dx = random.randrange(-9,9)
            #dy = random.randrange(-9,9)
            dx = 0
            dy = 0
            i+=1
            line_col =colors[i%5]
            for line in poly.lines:
                lineitem = QtGui.QGraphicsLineItem(
                        SCALE*line.start.x+dx+CIRCLE_SIZE/2, -SCALE*line.start.y+dy+CIRCLE_SIZE/2,
                        SCALE*line.end.x+dx+CIRCLE_SIZE/2, -SCALE*line.end.y+dy+CIRCLE_SIZE/2)
                lineitem.setPen(line_col)
                self.addItem(lineitem)
        for n, p in draw.positions.items():
            #draw point
            debug('drawing node %s at (%d,%d)' % (n, p.x, p.y))
            circle = QtGui.QGraphicsEllipseItem(
                SCALE*p.x, -SCALE*p.y, CIRCLE_SIZE, CIRCLE_SIZE)
            circle.setToolTip(n)
            circle.setBrush(QtGui.QBrush(QtCore.Qt.yellow))
            circle.setZValue(1) #they're on top of lines
            self.addItem(circle)
            label = QtGui.QGraphicsTextItem(n)
            label.setPos(SCALE*p.x + CIRCLE_SIZE, -SCALE*p.y)
            label.setZValue(2) #they're on top of everythin
            self.addItem(label)

        for x in range(-5,5):
            c = QtGui.QGraphicsTextItem(str(x))
            c.setPos(SCALE*x, SCALE*1)
            c.setZValue(3)
            self.addItem(c)


    

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

        self.main_vbox.addWidget(self.view)
        self.main_vbox.addLayout(self.input_hbox)

        widg = QtGui.QWidget()
        self.setCentralWidget(widg)
        self.centralWidget().setLayout(self.main_vbox)
    
    def on_ok(self):
        scene = GraphScene()
        start_time = time.time()
        graph = st.build_graph()
        stgraph = st.test1()
        draw = st.Drawing(stgraph)
        try:
            draw.draw()
        except Exception, e: 
            print 'EXCEPTION'
            print e
        end_time = time.time()
        print 'Computing time: %.3f' % (end_time - start_time)
        scene.from_drawing(draw)
        self.view.setScene(scene)
        self.view.resetCachedContent()


if __name__ == '__main__':
    App = QtGui.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(App.exec_())
