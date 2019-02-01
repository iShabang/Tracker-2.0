from PyQt5 import QtWidgets, QtGui, QtCore
from decimal import getcontext, Decimal
import datetime

import dbfunctions
import models
import uitools

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def setupWindow(self):
        self.setWindowTitle("Full Test Application")
        self.setGeometry(10,10,600,400)
        self.centerScreen()

    def getProperties(self):
        self.categories = dbfunctions.GetAllCategories()
        self._categoriesDict = {}
        for row in self.categories:
            self._categoriesDict[row[1]] = row[0]
        self.headers = ["ID", "Name", "Date", "Price", "Category"]
        self._headersDict = dict(zip(self.headers,range(len(self.headers))))    

    def buildTable(self, data):
        self.mainTable = QtWidgets.QTableView()
        self.tableModel = models.tableModel(data=data, headers=self.headers)
        self.proxyModel = QtCore.QSortFilterProxyModel()
        self.proxyModel.setSourceModel(self.tableModel)
        self.mainTable.setModel(self.proxyModel)
        self.stretchTableHeaders(self.mainTable, 5)
        self.mainTable.setSortingEnabled(True)
        self.proxyModel.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.mainTable.sortByColumn(0, QtCore.Qt.AscendingOrder)

    def buildStatList(self, data):
        self.statList = QtWidgets.QTableView()
        self.listModel = models.listModel(data=data)
        self.statList.setModel(self.listModel)

    def setCurrentDateInterval(self, lowdate, highdate): 
        self.currentDateInterval = (lowdate,highdate)

    def getTransactions(self):
        self.transactions = dbfunctions.GetTransByDateInterval(lowdate=self.currentDateInterval[0], highdate=self.currentDateInterval[1])
      
    def initUI(self):
        self.setupWindow()
        self.setCurrentDate()
        self.buildMenu()
        self.getProperties()
        self.setCurrentDateInterval("2019-01-00", self.currentDate)
        self.buildTable()
        self._mapper = QtWidgets.QDataWidgetMapper()
        self.setCurrentDate()

        """Info Labels Setup"""
        incomeCategory = uitools.findIncomeCategory()
        self.amountSpent = sum(uitools.getColumnSpent(self.transactions, 3, incomeCategory))
        self.amountEarned = sum(uitools.getColumnEarned(self.transactions, 3, incomeCategory))
        self.amountSaved = self.amountEarned - self.amountSpent
        self.buildStatList(data=[[str(self.amountSpent),str(self.amountEarned),str(self.amountSaved)]])
        self.spentLabel = QtWidgets.QLabel('Spent:')
        self.earnedLabel = QtWidgets.QLabel('Earned:')
        self.savedLabel = QtWidgets.QLabel('Saved:')
        self.spentEdit = QtWidgets.QLineEdit()
        self.earnedEdit = QtWidgets.QLineEdit()
        self.savedEdit = QtWidgets.QLineEdit()
        self._mapper.setModel(self.listModel)
        self._mapper.addMapping(self.spentEdit, 0)
        self._mapper.addMapping(self.earnedEdit, 1)
        self._mapper.addMapping(self.savedEdit, 2)
        self._mapper.toFirst()

        """Filter Section"""
        self.filterComboBox = QtWidgets.QComboBox()
        for header in self.headers:
            self.filterComboBox.addItem(header)
        self.filterEdit = QtWidgets.QLineEdit()
        self.filterEdit.setPlaceholderText('Enter Text')

        def filterTable():
            self.proxyModel.setFilterKeyColumn(self._headersDict[self.filterComboBox.currentText()])
            self.proxyModel.setFilterRegExp(self.filterEdit.text())

        self.filterEdit.textChanged.connect(filterTable)

        """Delete Method"""

        """Buttons"""
        self.addTransBttn = QtWidgets.QPushButton('Add Transaction', self)
        self.addTransBttn.clicked.connect(self.openAddDialog)
        self.addCatBttn = QtWidgets.QPushButton('Add Category', self)
        self.addCatBttn.clicked.connect(self.openAddCatDialog)
        button_del = QtWidgets.QPushButton('Delete Selected', self)
        button_del.clicked.connect(self.deleteRows)

        """Top Grid"""
        self.topGrid = QtWidgets.QGridLayout()
        self.topGrid.addWidget(self.spentLabel,0,0)
        self.topGrid.addWidget(self.earnedLabel,1,0)
        self.topGrid.addWidget(self.savedLabel,2,0)
        self.topGrid.addWidget(self.addTransBttn,3,0)
        self.topGrid.addWidget(self.addCatBttn,3,1)
        self.topGrid.addWidget(self.spentEdit,0,1)
        self.topGrid.addWidget(self.earnedEdit,1,1)
        self.topGrid.addWidget(self.savedEdit,2,1)
        self.topGrid.addWidget(self.filterComboBox,3,2)
        self.topGrid.addWidget(self.filterEdit,3,3)
        self.topGrid.addWidget(button_del,3,4)
        self.topGrid.setColumnStretch(3,1)
        self.topGrid.setColumnStretch(4,1)

        """Main Layout"""
        self._mainvbox = QtWidgets.QVBoxLayout()
        self._mainvbox.addLayout(self.topGrid)
        self._mainvbox.addWidget(self.mainTable)
        self._mainWidget = QtWidgets.QWidget()
        self._mainWidget.setLayout(self._mainvbox)
        self.setCentralWidget(self._mainWidget)

    def setCurrentDate(self):
        self.currentDate = QtCore.QDate.currentDate()

    def centerScreen(self):
        rectangle = self.frameGeometry()
        centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
        rectangle.moveCenter(centerPoint)
        self.move(rectangle.topLeft())

    def buildMenu(self):
        self.mainMenu = self.menuBar()
        self.fileMenu = self.mainMenu.addMenu('File')
        self.fileMenu.addAction('Print')
        self.editMenu = self.mainMenu.addMenu('Edit')
        self.editMenu.addAction('Copy')
        self.editMenu.addAction('Delete')
        self.reportMenu = self.mainMenu.addMenu('Report')
        self.reportMenu.addAction('Week')
        self.reportMenu.addAction('Month')
        self.reportMenu.addAction('Year')

    def DatePopup(self):
        dateEdit = QtWidgets.QDateEdit()
        dateEdit.setDate(self.currentDate)
        dateEdit.setCalendarPopup(True)
        dateEdit.setDisplayFormat('yyyy-MM-dd')
        return dateEdit
    
    def stretchTableHeaders(self, table, numColumns):
        header = table.horizontalHeader()
        for i in range(numColumns):
            header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)

    def deleteRows(self):
        selectedRows = self.mainTable.selectionModel().selectedRows()
        indices = []
        for i in selectedRows:
            indices.append(i.row())
        indices.sort()
        difference = 0
        for index in indices:
            row = index-difference
            self.tableModel.removeRows(row=row,count=1)
            difference += 1

    def openAddDialog(self):
        addWindow = QtWidgets.QDialog()
        addWindow.setWindowTitle("Adding Transaction")
        edit_name = QtWidgets.QLineEdit()
        edit_name.setPlaceholderText('Name')
        check_float = QtGui.QDoubleValidator()
        check_float.setDecimals(2)
        edit_amount = QtWidgets.QLineEdit()
        edit_amount.setValidator(check_float)
        edit_amount.setPlaceholderText('Price')
        comboBox_category = QtWidgets.QComboBox()
        for row in self.categories:
            comboBox_category.addItem(row[1])
        edit_date = self.DatePopup()
        addButton = QtWidgets.QPushButton('Submit', addWindow)
        cancelButton = QtWidgets.QPushButton('Cancel', addWindow)

        def submit():
            name = edit_name.text()
            date = edit_date.text()
            amount = edit_amount.text()
            category = comboBox_category.currentText()
            transaction = [name,date,float(amount), self._categoriesDict[category]]
            dbfunctions.AddTrans(values=transaction)
            addWindow.close()

        addButton.clicked.connect(submit)
        cancelButton.clicked.connect(addWindow.close)
        mainlayout = QtWidgets.QVBoxLayout()
        buttonlayout = QtWidgets.QHBoxLayout()
        buttonlayout.addWidget(addButton)
        buttonlayout.addWidget(cancelButton)
        mainlayout.addWidget(edit_name)
        mainlayout.addWidget(edit_amount)
        mainlayout.addWidget(comboBox_category)
        mainlayout.addWidget(edit_date)
        mainlayout.addLayout(buttonlayout)
        addWindow.setLayout(mainlayout)
        addWindow.exec_()
        
    def openAddCatDialog(self):
        addWindow = QtWidgets.QDialog()
        addWindow.setWindowTitle("Adding Category")
        edit_category = QtWidgets.QLineEdit()
        edit_category.setPlaceholderText('Category')
        checkBox_income = QtWidgets.QCheckBox('Income')
        addButton = QtWidgets.QPushButton('Submit', addWindow)
        cancelButton = QtWidgets.QPushButton('Cancel', addWindow)

        def submit():
            category = edit_category.text()
            income = 0
            if checkBox_income.isChecked():
                income = 1
            dbfunctions.AddCategory(name=category, income=income)
            addWindow.close()

        addButton.clicked.connect(submit)
        cancelButton.clicked.connect(addWindow.close)
        mainlayout = QtWidgets.QVBoxLayout()
        buttonlayout = QtWidgets.QVBoxLayout()
        buttonlayout.addWidget(addButton)
        buttonlayout.addWidget(cancelButton)
        mainlayout.addWidget(edit_category)
        mainlayout.addWidget(checkBox_income)
        mainlayout.addLayout(buttonlayout)
        addWindow.setLayout(mainlayout)
        addWindow.exec_()
