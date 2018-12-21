import sqlite3

def DbConnect(func):
    def wrapper(*args):
        connection = sqlite3.connect('tracker.db')
        cursor = connection.cursor()
        data = func(cursor,*args)
        connection.close()
        return data 
    return wrapper

@DbConnect
def AddTrans(cursor, values):
    cursor.execute("INSERT INTO trans(name, date, amount, cat_id) VALUES (?,?,?,?);", (values,))

@DbConnect
def AddManyTrans(cursor, values):
    cursor.executemany("INSERT INTO trans(name, date, amount, cat_id) VALUES (?,?,?,?);", values)

@DbConnect
def DelTrans(cursor, id_num):
    cursor.execute("DELETE FROM trans WHERE trans_id=?;", (id_num,))

@DbConnect
def AddCategory(cursor, name):
    cursor.execute("INSERT INTO category(name) VALUES(?)", (name,))

@DbConnect
def DelCategory(cursor, cat_id):
    cursor.execute("DELETE FROM category WHERE cat_id=?;", (cat_id,))

@DbConnect
def AddBill(cursor, values):
    cursor.execute("INSERT INTO bills(due_date,amount_due,cat_id,last_payment) VALUES (?,?,?,?)", (values,))

@DbConnect
def DelBill(cursor, bill_id):
    cursor.execute("DELETE FROM bills WHERE bill_id=?", (bill_id,))

@DbConnect
def GetTransByDateInterval(cursor, lowdate, highdate):
    cursor.execute('''
    SELECT trans_id, name, date, amount, cat_id
    FROM trans
    WHERE date >= ? AND date <= ?''', (lowdate,highdate))
    return cursor.fetchall()

@DbConnect
def GetTransByName(cursor, name):
    cursor.execute('''
    SELECT trans_id, name, date, amount, cat_id
    FROM trans
    WHERE name LIKE ?''', (name,))
    return cursor.fetchall()

@DbConnect
def GetTransByNameDate(cursor, name, lowdate, highdate):
    cursor.execute('''
    SELECT trans_id, name, date, amount, cat_id
    FROM trans
    WHERE date >= ? AND date <= ?
    AND name LIKE ?''', (lowdate,highdate, name))
    return cursor.fetchall()

@DbConnect
def GetTransByCategory(cursor, cat_id):
    cursor.execute('''
    SELECT trans_id, name, date, amount, cat_id
    FROM trans
    WHERE cat_id=?''', (cat_id,))
    return cursor.fetchall()

@DbConnect
def GetTransByCategoryDate(cursor, cat_id, lowdate, highdate):
    cursor.execute("""
    SELECT trans_id, name, date, amount, cat_id
    FROM trans
    WHERE date >= ? AND date <= ?
    AND cat_id=?""", (lowdate, highdate, cat_id))
    return cursor.fetchall()

def DateSearchString(year, month, day):
    search_string = "{}-{}-{}".format(year, month, day)
    return search_string

def NameSearchString(name):
    search_string="%{}%".format(name)
    return search_string
    

