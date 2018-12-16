from mainwindow import MainWindow
from PyQt5.QtWidgets import QApplication

app = QApplication([])
gui = MainWindow()
gui.show()
app.exec_()
