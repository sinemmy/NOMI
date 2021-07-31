import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction


class Test(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("HELLO WORLD")
        self.resize(400, 300)
        self.addWidget()

    def addWidget(self):
        self.statusBar().showMessage("Welcome All")

        menu = self.menuBar()

        fmen = menu.addMenu('File')



def myfun():

    print("Hello")
    print("PURPLE")

myfun()

#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     myGUI = Test() # initialize the GUI by making a Test object
#     myGUI.show()
#     sys.exit(app.exec_())