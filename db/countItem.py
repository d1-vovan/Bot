import sqlite3

def getAllItemIdName():
    items = []
    with sqlite3.connect('db\dbMeridian.db') as db:
        cursor = db.cursor()
        cursor.execute("""SELECT id, Name from Item """)
        items = cursor.fetchall()

    return items

def getCountItem(id):
    count = 0
    with sqlite3.connect('db\dbMeridian.db') as db:
        cursor = db.cursor()
        cursor.execute(f"SELECT InStorage FROM Item WHERE id = ?", (id,))
        count = cursor.fetchone()

    return count