from decimal import getcontext, Decimal
import dbfunctions

def getColumnSpent(data, column, incomeCategoryList):
    spentList = []
    for row in data:
        for i in incomeCategoryList:
            if row[4] != i:
                    spentList.append(Decimal(row[column]).quantize(Decimal('0.01')))
    return spentList

def getColumnEarned(data, column, incomeCategoryList):
    earnedList = []
    for row in data:
        for i in incomeCategoryList:
            if row[4] == i:
                earnedList.append(Decimal(row[column]).quantize(Decimal('0.01')))
    return earnedList

def findIncomeCategory():
    incomeCategoryList = []
    categoryData = dbfunctions.GetAllCategories()
    for row in categoryData:
        if row[2] == 1:
            incomeCategoryList.append(row[1])
    return incomeCategoryList

