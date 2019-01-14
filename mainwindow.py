from PyQt5 import QtWidgets, QtGui, QtCore

import dbfunctions
import models

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
      
    def initUI(self):
        self.setWindowTitle("Full Test Application")
        self.setGeometry(10,10,600,400)
        self.move(centerScreen(self))
        self.buildMenu()

        self.categories = dbfunctions.GetAllCategories()

        """Table Setup"""
        data = dbfunctions.GetTransByDateInterval(lowdate='2017-00-00', highdate='2020-00-00')
        headers = ["ID", "Name", "Date", "Price", "Category"]
        mainTable = QtWidgets.QTableView()
        tableModel = models.tableModel(data=data, headers=headers)
        proxyModel = QtCore.QSortFilterProxyModel()
        proxyModel.setSourceModel(tableModel)
        mainTable.setModel(proxyModel)
        stretchTableHeaders(mainTable, 5)
        mainTable.setSortingEnabled(True)
        mainTable.sortByColumn(0, QtCore.Qt.AscendingOrder)

        """Info Labels Setup"""
        incomeCategory = findIncomeCategory()
        amountSpent = sum(getColumnSpent(data, 3, incomeCategory))
        amountEarned = sum(getColumnEarned(data, 3, incomeCategory))
        amountSaved = amountEarned - amountSpent
        label_totalSpent = QtWidgets.QLabel('Total Spent:')
        label_totalEarned = QtWidgets.QLabel('Total Earned:')
        label_saved = QtWidgets.QLabel('Saved:')
        label_totalSpentValue = QtWidgets.QLabel(str(amountSpent))
        label_totalEarnedValue = QtWidgets.QLabel(str(amountEarned))
        label_totalSavedValue = QtWidgets.QLabel(str(amountSaved))

        """Buttons"""
        button_add = QtWidgets.QPushButton('Add Transaction', self)
        button_add.clicked.connect(self.openAddDialog)
        button_addCategory = QtWidgets.QPushButton('Add Category', self)
        button_addCategory.clicked.connect(self.openAddCatDialog)

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
        grid_insert.setColumnStretch(2,1)

        """Main Layout"""
        mainvbox = QtWidgets.QVBoxLayout()
        mainvbox.addLayout(grid_insert)
        mainvbox.addWidget(mainTable)
        self.mainWidget = QtWidgets.QWidget()
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
        calendar = QtWidgets.QCalendarWidget()

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
        edit_date = DatePopup()
        addButton = QtWidgets.QPushButton('Submit', addWindow)

        def submit():
            name = edit_name.text()
            date = edit_date.text()
            amount = edit_amount.text()
            category = comboBox_category.currentText()
            data = [name,date,float(amount),1]
            print(data)
            dbfunctions.AddTrans(values=(name,date,amount,1))
            addWindow.close()

        addButton.clicked.connect(submit)
        mainlayout = QtWidgets.QVBoxLayout()
        mainlayout.addWidget(edit_name)
        mainlayout.addWidget(edit_amount)
        mainlayout.addWidget(comboBox_category)
        mainlayout.addWidget(edit_date)
        mainlayout.addWidget(addButton)
        addWindow.setLayout(mainlayout)
        addWindow.exec_()
        
    def openAddCatDialog(self):
        addWindow = QtWidgets.QDialog()
        addWindow.setWindowTitle("Adding Category")
        edit_category = QtWidgets.QLineEdit()
        edit_category.setPlaceholderText('Category')
        addButton = QtWidgets.QPushButton('Submit', addWindow)

        def submit():
            category = edit_category.text()
            print(category)
            dbfunctions.AddCategory(name=(category))
            addWindow.close()

        addButton.clicked.connect(submit)
        mainlayout = QtWidgets.QVBoxLayout()
        mainlayout.addWidget(edit_category)
        mainlayout.addWidget(addButton)
        addWindow.setLayout(mainlayout)
        addWindow.exec_()

def DatePopup():
    dateEdit = QtWidgets.QDateEdit()
    dateEdit.setDate(QtCore.QDate.currentDate())
    dateEdit.setCalendarPopup(True)
    dateEdit.setDisplayFormat('yyyy-MM-dd')
    return dateEdit

def centerScreen(widget):
    rectangle = widget.frameGeometry()
    centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
    rectangle.moveCenter(centerPoint)
    return rectangle.topLeft()

def transactionTable(transactions):
    table = QtWidgets.QTableWidget()
    table.setRowCount(0)
    table.setColumnCount(5)
    table.setHorizontalHeaderLabels(["ID", "Name", "Date", "Price", "Category"])
    stretchTableHeaders(table, 5)
    for row_number, row_data in enumerate(transactions):
        table.insertRow(row_number)
        for column_number, column_data in enumerate(row_data):
            table.setItem(row_number, column_number, QTableWidgetItem(str(column_data)))
    table.setSortingEnabled(True)
    return table

def stretchTableHeaders(table, numColumns):
    header = table.horizontalHeader()
    for i in range(numColumns):
        header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)

def getColumnSpent(data, column, incomeCategoryList):
    spentList = []
    for row in data:
        for i in incomeCategoryList:
            if row[4] != i:
                    spentList.append(row[column])
    return spentList

def getColumnEarned(data, column, incomeCategoryList):
    earnedList = []
    for row in data:
        for i in incomeCategoryList:
            if row[4] == i:
                earnedList.append(row[column])
    return earnedList

def findIncomeCategory():
    incomeCategoryList = []
    categoryData = dbfunctions.GetAllCategories()
    for row in categoryData:
        if row[2] == 1:
            incomeCategoryList.append(row[1])
    return incomeCategoryList


