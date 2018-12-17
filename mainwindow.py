from PyQt5.QtWidgets import (QApplication, QTabWidget, QWidget, QVBoxLayout,
                            QLabel, QLineEdit, QTableWidget, QMainWindow, QPushButton,
                            QHBoxLayout, QGridLayout, QDesktopWidget, QTableWidgetItem)
import sqlite3
from dbfunctions import *

class MainWindow(QMainWindow):
    def __init__(self):
       super().__init__()
       self.initUI()
      
    def initUI(self):
        self.setWindowTitle("Full Test Application")
        self.setGeometry(10,10,600,400)
        self.move(centerScreen(self))
        self.buildMenu()

        data = testData()
        maintable = transactionTable(data)

        mainvbox = QVBoxLayout()
        mainvbox.addWidget(maintable)

        self.mainWidget = QWidget()
        self.mainWidget.setLayout(mainvbox)
        self.setCentralWidget(self.mainWidget)


    def buildMenu(self):
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        editMenu = mainMenu.addMenu('Edit')
        viewMenu = mainMenu.addMenu('View')
        searchMenu = mainMenu.addMenu('Search')
        toolsMenu = mainMenu.addMenu('Tools')
        helpMenu = mainMenu.addMenu('Help')
        fileMenu.addAction('Test')


class transactionTab(QWidget):
    def __init__(self,table):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(table)
        self.setLayout(layout)


def centerScreen(widget):
    rectangle = widget.frameGeometry()
    centerPoint = QDesktopWidget().availableGeometry().center()
    rectangle.moveCenter(centerPoint)
    return rectangle.topLeft()

def transactionTable(transactions):
    tableWidget = QTableWidget()
    tableWidget.setRowCount(0)
    tableWidget.setColumnCount(5)
    for row_number, row_data in enumerate(transactions):
        tableWidget.insertRow(row_number)
        for column_number, column_data in enumerate(row_data):
            tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(column_data)))
    return tableWidget

def testData():
    connection = sqlite3.connect('tracker.db')
    c = connection.cursor()
    data = GetTransByDateInterval(c, '2018-11-00', '2018-11-32')
    connection.close()
    return data

