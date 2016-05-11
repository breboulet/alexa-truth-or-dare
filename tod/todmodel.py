import json
import sqlite3


class TodModel:
    def __init__(self):
        self.dbConnection = TodModel.createdb()

    @staticmethod
    def createdb():
        dbconnection = sqlite3.connect(":memory:")
        cursor = dbconnection.cursor()
        cursor.execute("CREATE TABLE categories ( id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE )")
        cursor.execute("CREATE TABLE questions ( sentence TEXT NOT NULL UNIQUE, type TEXT NOT NULL, "
                       "categoryid INTEGER, FOREIGN KEY(categoryid) REFERENCES categories(id) )")
        dbconnection.commit()
        return dbconnection

    def addcategory(self, name):
        cursor = self.dbConnection.cursor()
        cursor.execute("INSERT INTO categories (name) VALUES (?)", (name,))
        self.dbConnection.commit()
        return cursor.lastrowid

    # def addquestion(self, sentence, truthOrDare, categoryid):

    def getallcategories(self):
        cursor = self.dbConnection.cursor()
        cursor.execute("SELECT * FROM categories")
        return cursor.fetchall()

    def getallquestions(self):
        cursor = self.dbConnection.cursor()
        cursor.execute("SELECT * FROM questions")
        return cursor.fetchall()
