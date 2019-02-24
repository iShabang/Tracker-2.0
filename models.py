from PyQt5 import QtCore, QtWidgets, QtGui
import dbfunctions as db


class StatModel(QtCore.QAbstractTableModel):
    def __init__(self, data = [[]], parent = None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self._data = data
    
    def isEmpty(self):
        if len(self._data) == 0:
            return True
        else:
            return False

    def rowCount(self, parent):
        return len(self._data)

    def columnCount(self, parent):
        if self.isEmpty():
            return 0
        return len(self._data[0])

    def data(self, index, role):

        if role == QtCore.Qt.DisplayRole or QtCore.Qt.EditRole:
            row = index.row()
            column = index.column()
            value = self._data[row][column]
            return value

    def removeRows(self, row, count, parent = QtCore.QModelIndex()):
        self.beginRemoveRows(parent, row, row + count - 1) 

        for i in range(count):
            del self._data[row]

        self.endRemoveRows()
        return True

    def changeData(self, data):
        self._data = data
        spentIndex = self.createIndex(0,0)
        earnedIndex = self.createIndex(0,1)
        savedIndex = self.createIndex(0,2)
        self.dataChanged.emit(spentIndex, spentIndex)
        self.dataChanged.emit(earnedIndex, earnedIndex)
        self.dataChanged.emit(savedIndex, savedIndex)


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data = [[]], headers = [], parent = None):
        QtCore.QAbstractTableModel.__init__(self,parent)
        self._data = data
        self._headers = headers

    def isEmpty(self):
        if len(self._data) == 0:
            return True

    def rowCount(self, parent = None):
        return len(self._data)

    def columnCount(self, parent = None):
        if self.isEmpty():
            return 0
        return len(self._data[0])
    
    def flags(self,index):
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def data(self, index, role):
        if self.isEmpty():
            return None
        
        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            column = index.column()
            value = self._data[row][column]
            return value

        if role == QtCore.Qt.EditRole:
            return self._data[index.row()][index.column()]
    
    def setData(self, index, value, itemType, role = QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:
            rowIndex = index.row()
            colIndex = index.column()
            if self._data[rowIndex][colIndex] == value:
                return True
            self._data[rowIndex][colIndex] = value
            self.dataChanged.emit(index,index)
            row = self._data[rowIndex]
            cat_id = db.getCatID(row[4])[0]
            db.updateTrans(row[0],row[1],row[2],float(row[3]),cat_id)
            return True
        return False

    def insertRows(self, position, rows, data, parent = QtCore.QModelIndex()):
        self.beginInsertRows(parent, position, position + rows - 1)
        db.AddTrans(values=data)
        newEntry = db.getLastTrans()
        self._data.append(newEntry) 
        self.endInsertRows()
        return True


    def removeRows(self, row, count, itemType, cascade = False, parent = QtCore.QModelIndex()):
        self.beginRemoveRows(parent, row, row + count - 1) 

        if itemType == "trans":
            func = db.delTransByID
        elif itemType == "cat":
            func = db.delCategoryByID

        if cascade == True:
            cat_id = (self._data[row][0])
            db.delTransByCat(cat_id)

        for i in range(count):
            func(self._data[row][0])
            del self._data[row]

        self.endRemoveRows()
        return True

    def headerData(self, section, orientation, role):
        if self.isEmpty():
            return None

        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return self._headers[section]
            if orientation == QtCore.Qt.Vertical:
                return "  "

    def updateConstraint(self, rows):
        db.delTransByCat(self._data[row][0]) 


class floatProxyModel(QtCore.QSortFilterProxyModel):
    def lessThan(self, left, right):
        sourceLeft = self.sourceModel().data(left,role=QtCore.Qt.DisplayRole)
        sourceRight = self.sourceModel().data(right,role=QtCore.Qt.DisplayRole)
        try:
            return float(sourceLeft) < float(sourceRight)
        except: 
            pass

        return sourceLeft < sourceRight


class CatTableModel(TableModel):
    def __init__(self, data = [[]], headers = [], parent = None):
        super().__init__()
        self._data = data
        self._headers = headers

    def setData(self, index, value, itemType, role = QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:
            rowIndex = index.row()
            colIndex = index.column()
            if self._data[rowIndex][colIndex] == value:
                return True
            self._data[rowIndex][colIndex] = value
            self.dataChanged.emit(index,index)
            row = self._data[rowIndex]
            db.updateCat(row[0],row[1],row[2])
            return True
        return False

