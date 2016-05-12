import json
import sqlite3


class Model:
    def __init__(self):
        self.dbConnection = Model.createdb()

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
        categoryid = None
        try:
            cursor = self.dbConnection.cursor()
            cursor.execute("INSERT INTO categories (name) VALUES (?)", (name,))
            self.dbConnection.commit()
            categoryid = cursor.lastrowid
        except sqlite3.IntegrityError, e:
            print e
            categoryid = self.getcategoryid(name)
        finally:
            return categoryid

    def getcategoryid(self, categoryname):
        cursor = self.dbConnection.cursor()
        cursor.execute("SELECT id FROM categories WHERE name=?", (categoryname,))
        row = cursor.fetchone()
        if row is not None:
            return row[0]
        else:
            return None

    def getquestionid(self, question):
        cursor = self.dbConnection.cursor()
        cursor.execute("SELECT rowid FROM questions WHERE sentence=?", (question,))
        row = cursor.fetchone()
        if row is not None:
            return row[0]
        else:
            return None

    def getquestionsoftypeandcategory(self, truthordare, categoryid):
        cursor = self.dbConnection.cursor()
        cursor.execute("SELECT * FROM questions WHERE type=? and categoryid=?", (truthordare, categoryid))
        return cursor.fetchall()

    def addquestion(self, sentence, truthordare, categoryname):
        categoryid = self.addcategory(categoryname)
        if categoryid is not None:
            questionid = None
            try:
                cursor = self.dbConnection.cursor()
                cursor.execute("INSERT INTO questions (sentence, type, categoryid) VALUES (?,?,?)", (sentence,
                                                                                                     truthordare,
                                                                                                     categoryid))
                self.dbConnection.commit()
                questionid = cursor.lastrowid
            except sqlite3.IntegrityError, e:
                print e
                questionid = self.getquestionid(sentence)
            finally:
                return questionid
        else:
            return None

    def getallcategories(self):
        cursor = self.dbConnection.cursor()
        cursor.execute("SELECT * FROM categories")
        return cursor.fetchall()

    def getallquestions(self):
        cursor = self.dbConnection.cursor()
        cursor.execute("SELECT * FROM questions")
        return cursor.fetchall()

