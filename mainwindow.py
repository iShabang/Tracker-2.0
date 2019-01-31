from PyQt5 import QtWidgets, QtGui, QtCore
from decimal import getcontext, Decimal

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

    def buildTable(self):
        self.data = dbfunctions.GetTransByDateInterval(lowdate='2017-00-00', highdate='2020-00-00')
        self.mainTable = QtWidgets.QTableView()
        self.tableModel = models.tableModel(data=self.data, headers=self.headers)
        self.proxyModel = QtCore.QSortFilterProxyModel()
        self.proxyModel.setSourceModel(self.tableModel)
        self.mainTable.setModel(self.proxyModel)
        self.stretchTableHeaders(self.mainTable, 5)
        self.mainTable.setSortingEnabled(True)
        self.proxyModel.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.mainTable.sortByColumn(0, QtCore.Qt.AscendingOrder)

    def buildStatList(self, data):
        self.statList = QtWidgets.QListView()
        self.listModel = models.listModel(data = data)
        self.statList.setModel(self.listModel)

      
    def initUI(self):
        self.setupWindow()
        self.buildMenu()
        self.getProperties()
        self.buildTable()

        """Info Labels Setup"""
        incomeCategory = uitools.findIncomeCategory()
        amountSpent = sum(uitools.getColumnSpent(self.data, 3, incomeCategory))
        amountEarned = sum(uitools.getColumnEarned(self.data, 3, incomeCategory))
        amountSaved = amountEarned - amountSpent
        self.buildStatList(data=[amountSpent,amountEarned,amountSaved])
        label_totalSpent = QtWidgets.QLabel('Total Spent:')
        label_totalEarned = QtWidgets.QLabel('Total Earned:')
        label_saved = QtWidgets.QLabel('Saved:')
        label_totalSpentValue = QtWidgets.QLabel(str(amountSpent))
        label_totalEarnedValue = QtWidgets.QLabel(str(amountEarned))
        label_totalSavedValue = QtWidgets.QLabel(str(amountSaved))

        """Filter Section"""
        comboBox_filter = QtWidgets.QComboBox()
        for header in self.headers:
            comboBox_filter.addItem(header)
        edit_filter = QtWidgets.QLineEdit()
        edit_filter.setPlaceholderText('Enter Text')

        def filterTable():
            self.proxyModel.setFilterKeyColumn(self._headersDict[comboBox_filter.currentText()])
            self.proxyModel.setFilterRegExp(edit_filter.text())

        edit_filter.textChanged.connect(filterTable)

        """Delete Method"""
        def delete():
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


        """Buttons"""
        button_add = QtWidgets.QPushButton('Add Transaction', self)
        button_add.clicked.connect(self.openAddDialog)
        button_addCategory = QtWidgets.QPushButton('Add Category', self)
        button_addCategory.clicked.connect(self.openAddCatDialog)
        button_del = QtWidgets.QPushButton('Delete', self)
        button_del.clicked.connect(delete)

        """Top Grid"""
        grid_insert = QtWidgets.QGridLayout()
        grid_insert.addWidget(label_totalSpent,0,0)
        grid_insert.addWidget(label_totalEarned,1,0)
        grid_insert.addWidget(label_saved,2,0)
        grid_insert.addWidget(button_add,3,0)
        grid_insert.addWidget(button_addCategory,3,1)
        grid_insert.addWidget(label_totalSpentValue,0,1)
        grid_insert.addWidget(label_totalEarnedValue,1,1)
        grid_insert.addWidget(label_totalSavedValue,2,1)
        grid_insert.addWidget(comboBox_filter,3,2)
        grid_insert.addWidget(edit_filter,3,3)
        grid_insert.addWidget(button_del,3,4)
        grid_insert.setColumnStretch(3,1)
        grid_insert.setColumnStretch(4,1)

        """Main Layout"""
        mainvbox = QtWidgets.QVBoxLayout()
        mainvbox.addLayout(grid_insert)
        mainvbox.addWidget(self.mainTable)
        self.mainWidget = QtWidgets.QWidget()
        self.mainWidget.setLayout(mainvbox)
        self.setCentralWidget(self.mainWidget)

    def centerScreen(self):
        rectangle = self.frameGeometry()
        centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
        rectangle.moveCenter(centerPoint)
        self.move(rectangle.topLeft())

    def buildMenu(self):
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        editMenu = mainMenu.addMenu('Edit')
        viewMenu = mainMenu.addMenu('View')
        searchMenu = mainMenu.addMenu('Search')
        toolsMenu = mainMenu.addMenu('Tools')
        helpMenu = mainMenu.addMenu('Help')
        fileMenu.addAction('Test')

    def DatePopup(self):
        dateEdit = QtWidgets.QDateEdit()
        dateEdit.setDate(QtCore.QDate.currentDate())
        dateEdit.setCalendarPopup(True)
        dateEdit.setDisplayFormat('yyyy-MM-dd')
        return dateEdit
    
    def stretchTableHeaders(self, table, numColumns):
        header = table.horizontalHeader()
        for i in range(numColumns):
            header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)

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
            self.data = [name,date,float(amount), self._categoriesDict[category]]
            dbfunctions.AddTrans(values=self.data)
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
