import mysql.connector
from classes import COEFFS, Item

db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "root",
    database = "Items"
)

cursor = db.cursor()

# cursor.execute("CREATE DATABASE Items")
#cursor.execute("CREATE TABLE ItemsInfo (name varchar(50), price smallint, quality float, itemID int AUTO_INCREMENT PRIMARY KEY)")

def insertItem(item):
    name = item.item
    price = item.price
    quality = item.quality
    cursor.execute("INSERT INTO ItemsInfo (name, price, quality) VALUES (%s, %s, %s)", (name, price, quality))
    db.commit()

def getItem(id):
    cursor.execute("SELECT * FROM ItemsInfo WHERE itemID = %s", (id))
    itemInfo = cursor.fetchone()

    if itemInfo:
        return itemInfo
    return "Такого товара нет"

def getItems():
    cursor.execute("SELECT * FROM ItemsInfo")
    for x in cursor:
        name, price, quality, itemID = x
        print("Название: {} \n Цена: {} \n Качество: {} \n ID: {}".format(name, price, quality, itemID))

def makeItems():
    cursor.execute("SELECT * FROM ItemsInfo")

    items = []

    for x in cursor:
        name, price, quality, itemID = x
        newItem = Item(name)
        newItem.price = price
        newItem.quality = quality
    
    items.append(newItem)
    return(items)

def deleteItems():
    cursor.execute("DELETE FROM ItemsInfo")
    cursor.execute("ALTER TABLE ItemsInfo AUTO_INCREMENT = 1")
    db.commit()

def updateItem(new_price, new_quality, id):
    cursor.execute("UPDATE ItemsInfo SET price = %s, quality = %s WHERE itemID = %s", (new_price, new_quality, id))
    db.commit()

# cursor.execute("DELETE FROM ItemsInfo")
# cursor.execute("ALTER TABLE ItemsInfo AUTO_INCREMENT = 1")
# db.commit()