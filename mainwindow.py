from PyQt5.QtWidgets import (QApplication, QTabWidget, QWidget, QVBoxLayout,
                            QLabel, QLineEdit, QTableWidget, QMainWindow, QPushButton,
                            QHBoxLayout, QGridLayout, QDesktopWidget, QTableWidgetItem,
                            QAbstractScrollArea, QHeaderView, QSizePolicy, QComboBox,
                            QCalendarWidget, QDateEdit)

from PyQt5.QtCore import QDate

from PyQt5.QtGui import QDoubleValidator

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

        comboBox_category = QComboBox()
        comboBox_category.addItem('Category 1')
        comboBox_category.addItem('Category 2')
        comboBox_category.addItem('Category 3')

        edit_name = QLineEdit()
        edit_date = QLineEdit()

        check_float = QDoubleValidator()
        check_float.setDecimals(2)
        edit_amount = QLineEdit()
        edit_amount.setValidator(check_float)

        button_add = QPushButton('Add', self)

        dateSelect = DatePopup()

        label_totalSpent = QLabel('Total Spent:')
        label_info1 = QLabel('Info 1:')
        label_info2 = QLabel('Info 2:')
        label_info3 = QLabel('Info 3:')

        grid_insert = QGridLayout()
        grid_insert.addWidget(label_name,1,0)
        grid_insert.addWidget(label_date,2,0)
        grid_insert.addWidget(label_amount,3,0)
        grid_insert.addWidget(label_category,4,0)
        grid_insert.addWidget(edit_name,1,1)
        grid_insert.addWidget(dateSelect,2,1)
        grid_insert.addWidget(edit_amount,3,1)
        grid_insert.addWidget(comboBox_category,4,1)
        grid_insert.addWidget(label_totalSpent,1,2)
        grid_insert.addWidget(label_info1,2,2)
        grid_insert.addWidget(label_info2,3,2)
        grid_insert.addWidget(label_info3,4,2)
        grid_insert.addWidget(button_add,5,0,5,2)
        grid_insert.setColumnStretch(0,0)
        grid_insert.setColumnStretch(1,1)
        grid_insert.setColumnStretch(2,3)

        mainvbox = QVBoxLayout()
        mainvbox.addLayout(grid_insert)
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

    def calendarPopup():
        calendar = QCalendarWidget()


class transactionTab(QWidget):
    def __init__(self,table):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(table)
        self.setLayout(layout)


def DatePopup():
    dateEdit = QDateEdit()
    dateEdit.setDate(QDate.currentDate())
    dateEdit.setCalendarPopup(True)
    dateEdit.setDisplayFormat('yyyy/MM/dd')
    return dateEdit

def centerScreen(widget):
    rectangle = widget.frameGeometry()
    centerPoint = QDesktopWidget().availableGeometry().center()
    rectangle.moveCenter(centerPoint)
    return rectangle.topLeft()

def transactionTable(transactions):
    table = QTableWidget()
    table.setRowCount(0)
    table.setColumnCount(5)
    table.setHorizontalHeaderLabels(["ID", "Name", "Date", "Price", "Category"])
    stretchTableHeaders(table, 5)
    for row_number, row_data in enumerate(transactions):
        table.insertRow(row_number)
        for column_number, column_data in enumerate(row_data):
            table.setItem(row_number, column_number, QTableWidgetItem(str(column_data)))
    return table

def stretchTableHeaders(table, numColumns):
    header = table.horizontalHeader()
    for i in range(numColumns):
        header.setSectionResizeMode(i, QHeaderView.Stretch)

def testData():
    connection = sqlite3.connect('tracker.db')
    c = connection.cursor()
    data = dbfunctions.GetTransByDateInterval(c, '2018-11-00', '2018-11-32')
    connection.close()
    return data

