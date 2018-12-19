from PyQt5.QtWidgets import (QApplication, QTabWidget, QWidget, QVBoxLayout,
                            QLabel, QLineEdit, QTableWidget, QMainWindow, QPushButton,
                            QHBoxLayout, QGridLayout, QDesktopWidget, QTableWidgetItem,
                            QAbstractScrollArea, QHeaderView)

import PyQt5.QtWidgets

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

        label_name = QLabel('Name')
        label_date = QLabel('Date')
        label_amount = QLabel('Amount')
        label_category = QLabel('Category')
        button_add = QPushButton('Add', self)

        edit_name = QLineEdit()
        edit_date = QLineEdit()
        edit_amount = QLineEdit()
        edit_category = QLineEdit()

        grid_insert = QGridLayout()
        grid_insert.addWidget(label_name,1,0)
        grid_insert.addWidget(label_date,2,0)
        grid_insert.addWidget(label_amount,3,0)
        grid_insert.addWidget(label_category,4,0)
        grid_insert.addWidget(edit_name,1,1)
        grid_insert.addWidget(edit_date,2,1)
        grid_insert.addWidget(edit_amount,3,1)
        grid_insert.addWidget(edit_category,4,1)
        grid_insert.addWidget(button_add,5,0,5,3)

        label_totalSpent = QLabel('Total Spent:')
        label_info1 = QLabel('Info 1:')
        label_info2 = QLabel('Info 2:')
        label_info3 = QLabel('Info 3:')
        grid_totals = QGridLayout()
        grid_totals.addWidget(label_totalSpent,1,0)
        grid_totals.addWidget(label_info1,1,1)
        grid_totals.addWidget(label_info2,2,0)
        grid_totals.addWidget(label_info3,2,1)

        hbox_topRow = QHBoxLayout()
        hbox_topRow.addLayout(grid_insert)
        hbox_topRow.addLayout(grid_totals)

        mainvbox = QVBoxLayout()
        mainvbox.addLayout(hbox_topRow)
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
    tableWidget.setHorizontalHeaderLabels(["ID", "Name", "Date", "Price", "Category"])
    header = tableWidget.horizontalHeader()
    header.setSectionResizeMode(0, QHeaderView.Stretch)
    header.setSectionResizeMode(1, QHeaderView.Stretch)
    header.setSectionResizeMode(2, QHeaderView.Stretch)
    header.setSectionResizeMode(3, QHeaderView.Stretch)
    header.setSectionResizeMode(4, QHeaderView.Stretch)
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

