import sqlite3

#Create/Open database file
conn = sqlite3.connect('tracker.db')

#create cursor object for execution methods
c = conn.cursor()

#create tables

c.execute('''CREATE TABLE IF NOT EXISTS category (
                cat_id INTEGER PRIMARY KEY,
                name TEXT);''')

c.execute('''CREATE TABLE IF NOT EXISTS trans (
                trans_id INTEGER PRIMARY KEY,
                name TEXT, 
                date TEXT, 
                amount REAL,
                cat_id INTEGER,
                FOREIGN KEY(cat_id)
                REFERENCES category(cat_id) ON DELETE SET NULL);''') 

c.execute('''CREATE TABLE IF NOT EXISTS bills (
                bill_id INTEGER PRIMARY KEY,
                due_date TEXT, 
                amount_due REAL, 
                cat_id INTEGER,
                last_payment INTEGER,
                FOREIGN KEY(cat_id) 
                REFERENCES category(cat_id) ON DELETE SET NULL,
                FOREIGN KEY(last_payment) 
                REFERENCES trans(trans_id) ON DELETE SET NULL);''')

#Commit/Save Changes
conn.commit()

#close the connection (ALWAYS ALWAYS DO THIS WHEN DONE)
conn.close()



