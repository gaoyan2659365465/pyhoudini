import sys
from PYBP.window.childWidget.PYBP_ChildWidget import *

if __name__ == "__main__":
    app=QApplication(sys.argv)
    widget=PYBP_ChildWidget(None)
    widget.show()
    sys.exit(app.exec_())