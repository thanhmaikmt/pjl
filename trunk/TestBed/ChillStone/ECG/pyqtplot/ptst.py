"""
Demonstrate the use of layouts to control placement of multiple plots / views /
labels


"""

## Add path to library (just for examples; you do not need this)
#import initExample

from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np

app = QtGui.QApplication([])
view = pg.GraphicsView()
l = pg.GraphicsLayout(border=(100,100,100))
view.setCentralItem(l)
view.show()
view.setWindowTitle('pyqtgraph example: GraphicsLayout')
view.resize(800,600)


## Add a sub-layout into the second row (automatic position)
## The added item should avoid the first column, which is already filled

l.nextRow()
l2 = l.addLayout(colspan=1, border=(50,0,0))
l2.setContentsMargins(10, 10, 10, 10)
l2.addLabel("Sub-layout: this layout demonstrates the use of shared axes and axis labels", colspan=1)
l2.nextRow()
p21 = l2.addPlot()
l2.nextRow()
p22 = l2.addPlot()
l2.nextRow()
p23 = l2.addPlot()
l2.nextRow()
p24 = l2.addPlot()
l2.nextRow()

l2.addLabel("HorizontalAxisLabel", col=0, colspan=1)

## hide axes on some plots



p21.plot([1,3,2,4,3,5])
p22.plot([1,3,2,4,3,5])
p23.plot([1,3,2,4,3,5])
p24.plot([1,3,2,4,3,5])



## Start Qt event loop unless running in interactive mode.

if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
