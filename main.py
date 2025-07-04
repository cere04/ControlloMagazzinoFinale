import sys
from PyQt6 import QtWidgets
from View.loginView import Finestra1


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    login = Finestra1()
    login.show()
    sys.exit(app.exec())

class MainWindow(QtWidgets.QMainWindow, Finestra1):
     def __init__(self, *args, obj=None, **kwargs):
         super().__init__(*args, **kwargs)
         self.setupUi(self)
app = QtWidgets.QApplication(sys.argv)
window = Finestra1()
window.show()
app.exec()
