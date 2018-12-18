from PyQt5.QtWidgets import (QApplication, QTabWidget, QWidget, QVBoxLayout,
                            QLabel, QLineEdit, QTableWidget, QMainWindow, QPushButton,
                            QHBoxLayout, QGridLayout, QDesktopWidget, QTableWidgetItem)

import sqlite3

import dbfunctions

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

        addName = QLabel('Name')
        addDate = QLabel('Date')
        addCategory = QLabel('Category')
        addButton = QPushButton('Add', self)

        nameEdit = QLineEdit()
        dateEdit = QLineEdit()
        categoryEdit = QLineEdit()

        grid_insert = QGridLayout()
        grid_insert.addWidget(addName,1,0)
        grid_insert.addWidget(addDate,2,0)
        grid_insert.addWidget(addCategory,3,0)
        grid_insert.addWidget(nameEdit,1,1)
        grid_insert.addWidget(dateEdit,2,1)
        grid_insert.addWidget(categoryEdit,3,1)
        grid_insert.addWidget(addButton,4,0,4,3)

        label_totalSpent = QLabel('Total Spent:')
        label_category1 = QLabel('Category1:')
        label_category2 = QLabel('Category2:')
        label_category3 = QLabel('Category3:')
        grid_totals = QGridLayout()
        grid_totals.addWidget(label_totalSpent,1,0)
        grid_totals.addWidget(label_category1,1,1)
        grid_totals.addWidget(label_category2,2,0)
        grid_totals.addWidget(label_category3,2,1)

        addhbox = QHBoxLayout()
        addhbox.addLayout(grid_insert)
        addhbox.addLayout(grid_totals)
        addhbox.addStretch(1)

        mainvbox = QVBoxLayout()
        mainvbox.addLayout(addhbox)
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
    data = dbfunctions.GetTransByDateInterval(c, '2018-11-00', '2018-11-32')
    connection.close()
    return data

