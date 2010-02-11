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


    

start_time = end_time = 0
class Window(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.showMaximized()
        
        self.view = QtGui.QGraphicsView()
        self.main_vbox = QtGui.QVBoxLayout()
                
        self.input_hbox = QtGui.QHBoxLayout()
        self.test1 = QtGui.QPushButton('Test 1')
        self.input_hbox.addWidget(self.test1)
        self.connect(self.test1, QtCore.SIGNAL('clicked()'), self.on_test1)
        self.testk4 = QtGui.QPushButton('Test K4')
        self.input_hbox.addWidget(self.testk4)
        self.connect(self.testk4, QtCore.SIGNAL('clicked()'), self.on_testk4)
        self.testk5 = QtGui.QPushButton('Test K5')
        self.input_hbox.addWidget(self.testk5)
        self.connect(self.testk5, QtCore.SIGNAL('clicked()'), self.on_testk5)
        self.testcycle = QtGui.QPushButton('Test cycle')
        self.input_hbox.addWidget(self.testcycle)
        self.connect(self.testcycle, QtCore.SIGNAL('clicked()'), self.on_testcycle)
        self.testrandom = QtGui.QPushButton('Test random')
        self.input_hbox.addWidget(self.testrandom)
        self.connect(self.testrandom, QtCore.SIGNAL('clicked()'), self.on_testrandom)

        self.spin_box = QtGui.QSpinBox()
        self.spin_box.setMaximum(40)
        self.spin_box.setMinimum(3)
        self.spin_box.setValue(6)
        self.input_hbox.addWidget(self.spin_box)

        self.main_vbox.addWidget(self.view)
        self.main_vbox.addLayout(self.input_hbox)

        widg = QtGui.QWidget()
        self.setCentralWidget(widg)
        self.centralWidget().setLayout(self.main_vbox)
    
    def draw(self, graph):
        global start_time
        global end_time
        self.view.setScene(None)
        stgraph = graph.st()
        draw = st.Drawing(stgraph)
        draw.draw()
        end_time = time.time()
        print 'Computing time: %.3f' % (end_time - start_time)
        scene = GraphScene()
        scene.from_drawing(draw)
        self.view.setScene(scene)
        self.view.resetCachedContent()

    def on_testk5(self):
        global start_time
        start_time = time.time()
        graph = st.build_graph_k5()
        self.draw(graph)
    def on_testk4(self):
        global start_time
        start_time = time.time()
        graph = st.build_graph_k4()
        self.draw(graph)
    def on_testcycle(self):
        global start_time
        start_time = time.time()
        graph = st.build_graph_cycle(self.spin_box.value())
        self.draw(graph)
    def on_testrandom(self):
        global start_time
        start_time = time.time()
        graph = st.build_graph_random(self.spin_box.value())
        self.draw(graph)
        debug(graph.generating_code())

    def on_test1(self):
        global start_time
        start_time = time.time()
        graph = st.build_graph1()
        self.draw(graph)


if __name__ == '__main__':
    App = QtGui.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(App.exec_())
