from PyQt5 import QtCore, QtWidgets, QtGui
import dbfunctions as db


class listModel(QtCore.QAbstractTableModel):
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

class tableModel(QtCore.QAbstractTableModel):
    def __init__(self, data = [[]], headers = [], parent = None):
        QtCore.QAbstractTableModel.__init__(self,parent)
        self._data = data
        self.__headers = headers

    def isEmpty(self):
        if len(self._data) == 0:
            return True

    def rowCount(self, parent = None):
        return len(self._data)

    def columnCount(self, parent = None):
        if self.isEmpty():
            return 0
        return len(self._data[0])

    def data(self, index, role):
        if self.isEmpty():
            return None
        
        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            column = index.column()
            value = self._data[row][column]
            return value

    def insertRows(self, position, rows, data, parent = QtCore.QModelIndex()):
        self.beginInsertRows(parent, position, position + rows - 1)
        db.AddTrans(values=data)
        newEntry = db.getLastTrans()
        self._data.append(newEntry) 
        self.endInsertRows()
        return True


    def removeRows(self, row, count, itemType, parent = QtCore.QModelIndex()):
        self.beginRemoveRows(parent, row, row + count - 1) 

        if itemType == "trans":
            func = db.delTransByID
        elif itemType == "cat":
            func = db.DelCategory

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
                return self.__headers[section]
            if orientation == QtCore.Qt.Vertical:
                return "  "

    def updateConstraint(self, rows):
        db.delTransByCat(self._data[row][0]) 


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    data = dbfunctions.GetTransByDateInterval(lowdate='2017-00-00', highdate='2019-00-00')
    headers = ["Transaction ID", "Name", "Date", "Amount", "Category"]

    tableView = QtWidgets.QTableView()
    tableView.show()
    tableModel = tableModel(data=data, headers=headers)
    tableModel.insertRows(0,1)
    tableView.setModel(tableModel)

    app.exec_()
