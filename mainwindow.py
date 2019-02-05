from PyQt5 import QtWidgets, QtGui, QtCore
from decimal import getcontext, Decimal
import datetime

import dbfunctions as db
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
        self.categories = db.GetAllCategories()
        self._categoriesDict = {}
        for row in self.categories:
            self._categoriesDict[row[1]] = row[0]
        self.headers = ["ID", "Name", "Date", "Price", "Category"]
        self._headersDict = dict(zip(self.headers,range(len(self.headers))))    
        self.incomeCategory = uitools.findIncomeCategory()

    def buildTable(self):
        self.mainTable = QtWidgets.QTableView()
        self.tableModel = models.tableModel(data=self.trans, headers=self.headers)
        self.proxyModel = QtCore.QSortFilterProxyModel()
        self.proxyModel.setSourceModel(self.tableModel)
        self.mainTable.setModel(self.proxyModel)
        if not self.isEmpty():
            self.stretchTableHeaders(self.mainTable, 5)
        self.mainTable.setSortingEnabled(True)
        self.proxyModel.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.mainTable.sortByColumn(0, QtCore.Qt.AscendingOrder)

    def buildStatList(self):
        if self.isEmpty():
            data = []
        else:
            amountSpent = sum(uitools.getColumnSpent(self.trans, 3, self.incomeCategory))
            amountEarned = sum(uitools.getColumnEarned(self.trans, 3, self.incomeCategory))
            amountSaved = amountEarned - amountSpent
            data = [[str(amountSpent),str(amountEarned),str(amountSaved)]]
        self.statList = QtWidgets.QTableView()
        self.listModel = models.listModel(data=data)
        self.statList.setModel(self.listModel)
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

    def setDateInterval(self, thisMonth = True, lowdate = None, highdate = None): 
        if not thisMonth:
            self.lowdate = lowdate
            self.highdate = highdate
        else:
            self.lowdate = self.currentDate.toString("yyyy-MM-00")
            self.highdate = self.currentDate.toString("yyyy-MM-dd")

    def getTransactions(self):
        self.trans = db.getTransByDate(lowdate=self.lowdate, highdate=self.highdate)

    def isEmpty(self):
        if len(self.trans) == 0:
            return True
        return False

    def headerComboBox(self):
        comboBox = QtWidgets.QComboBox()
        for header in self.headers:
            comboBox.addItem(header)
        return comboBox

    def buildFilter(self):
        self.filterComboBox = self.headerComboBox()
        self.filterEdit = QtWidgets.QLineEdit()
        self.filterEdit.setPlaceholderText('Enter Text')

        def filterTable():
            self.proxyModel.setFilterKeyColumn(self._headersDict[self.filterComboBox.currentText()])
            self.proxyModel.setFilterRegExp(self.filterEdit.text())

        self.filterEdit.textChanged.connect(filterTable)

    def initUI(self):
        self.setupWindow()
        self.setCurrentDate()
        self.setDateInterval()
        self.buildMenu()
        self.getProperties()
        self.getTransactions()
        self._mapper = QtWidgets.QDataWidgetMapper()
        self.buildTable()
        self.buildStatList()
        self.buildFilter()

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
            db.AddTrans(values=transaction)
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
            db.AddCategory(name=category, income=income)
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
