import sqlite3

def DbConnectQuery(func):
    def wrapper(**kwargs):
        connection = sqlite3.connect('tracker.db')
        cursor = connection.cursor()
        data = func(cursor,**kwargs)
        connection.close()
        return data
    return wrapper

def DbConnectAction(func):
    def wrapper(**kwargs):
        connection = sqlite3.connect('tracker.db')
        cursor = connection.cursor()
        func(cursor,**kwargs)
        connection.commit()
        connection.close()
    return wrapper

@DbConnectAction
def AddTrans(cursor, values):
    cursor.execute("INSERT INTO trans(name, date, amount, cat_id) VALUES (?,?,?,?);", values)

@DbConnectAction
def AddManyTrans(cursor, values):
    cursor.executemany("INSERT INTO trans(name, date, amount, cat_id) VALUES (?,?,?,?);", values)

@DbConnectAction
def DelTrans(cursor, id_num):
    cursor.execute("DELETE FROM trans WHERE trans_id=?;", (id_num,))

@DbConnectAction
def AddCategory(cursor, name, income):
    cursor.execute("INSERT INTO category(name, income) VALUES (?,?);", (name,income))

@DbConnectAction
def DelCategory(cursor, cat_id):
    cursor.execute("DELETE FROM category WHERE cat_id=?;", (cat_id,))

@DbConnectAction
def AddBill(cursor, values):
    cursor.execute("INSERT INTO bills(due_date,amount_due,cat_id,last_payment) VALUES (?,?,?,?)", (values,))

@DbConnectAction
def DelBill(cursor, bill_id):
    cursor.execute("DELETE FROM bills WHERE bill_id=?", (bill_id,))

@DbConnectQuery
def GetTransByDateInterval(cursor, lowdate, highdate):
    cursor.execute('''
    SELECT trans.trans_id, trans.name, trans.date, printf("%.2f", trans.amount), category.name
    FROM trans INNER JOIN category ON trans.cat_id = category.cat_id
    WHERE date >= ? AND date <= ?''',(lowdate,highdate))
    return cursor.fetchall()

@DbConnectQuery
def GetTransByName(cursor, name):
    cursor.execute('''
    SELECT trans.trans_id, trans.name, trans.date, trans.amount, category.name
    FROM trans INNER JOIN category ON trans.cat_id = category.cat_id
    WHERE name LIKE ?''', (name,))
    return cursor.fetchall()

@DbConnectQuery
def GetTransByNameDate(cursor, name, lowdate, highdate):
    cursor.execute('''
    SELECT trans.trans_id, trans.name, trans.date, trans.amount, category.name
    FROM trans INNER JOIN category ON trans.cat_id = category.cat_id
    WHERE date >= ? AND date <= ?
    AND name LIKE ?''', (lowdate,highdate, name))
    return cursor.fetchall()

@DbConnectQuery
def GetTransByCategory(cursor, cat_id):
    cursor.execute('''
    SELECT trans.trans_id, trans.name, trans.date, trans.amount, category.name
    FROM trans INNER JOIN category ON trans.cat_id = category.cat_id
    WHERE cat_id=?''', (cat_id,))
    return cursor.fetchall()

@DbConnectQuery
def GetTransByCategoryDate(cursor, cat_id, lowdate, highdate):
    cursor.execute("""
    SELECT trans.trans_id, trans.name, trans.date, trans.amount, category.name
    FROM trans INNER JOIN category ON trans.cat_id = category.cat_id
    WHERE date >= ? AND date <= ?
    AND cat_id=?""", (lowdate, highdate, cat_id))
    return cursor.fetchall()

@DbConnectQuery
def GetAllCategories(cursor):
    cursor.execute("""
    SELECT cat_id, name, income
    FROM category""")
    return cursor.fetchall()

def DateSearchString(year, month, day):
    search_string = "{}-{}-{}".format(year, month, day)
    return search_string

def NameSearchString(name):
    search_string="%{}%".format(name)
    return search_string
    

