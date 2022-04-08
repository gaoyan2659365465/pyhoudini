import sys
from examples import *

if __name__ == "__main__":
    app=QApplication(sys.argv)
    widget=BlueprintWindow()
    widget.show()
    sys.exit(app.exec_())
