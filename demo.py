from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from widget.store.HoudiniStore import HoudiniStoreScrollArea

if __name__ == "__main__":
    import sys
    app=QApplication(sys.argv)
    pyhwidget=HoudiniStoreScrollArea()
    pyhwidget.show()
    sys.exit(app.exec_())