import sqlite3
import time
import secrets

#Я ненавижу писать запросы LMAO, т.к у нас нет никакого способа проверить работоспособность модуля, т.к нет самого казино.
#Завтра, я буду тестить скрипт в консоси. так что код модуля БД у нас есть, а вот работает ли он вообще яхз.
#P.S: Хотел выебнуться и написать на английском комент, но решил не портить тебе зрение своим английским. По этому испорчу тебе его мои русским
#P.P.S: Тяжело жить без подствеки ошибок в словах KEkw
class DB:
    def __init__(self, fileName, logger):
        self.conn = sqlite3.connect(fileName)
        self.cur = self.conn.cursor()
        self.tokenConn = sqlite3.connect(":memory:")
        self.tokenCur = self.tokenConn.cursor()

        self.logger: logger = logger

        self.cur.execute("""CREATE TABLE IF NOT EXISTS casino (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT,
        cash INTEGER,
        dateReg TEXT,
        dateLogin TEXT    
        )""")
        self.tokenCur.execute("""CREATE TABLE IF NOT EXISTS token (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        uToken TEXT
        )""")
        self.conn.commit()
        self.tokenConn.commit()

    def changeCash(self, id, deltaCash):
        self.cur.execute("SELECT cash FROM casino WHERE id = ?", (id,))
        result = self.cur.fetchone()[0]
        result += deltaCash
        self.cur.execute(f"UPDATE casino SET cash = ? WHERE id = {id}", (result))
        self.conn.commit()

    def Logining(self, username, password, logining=False, creatingToken=False):
        self.cur.execute("SELECT password FROM casino WHERE username = ?", (username,))
        if password == self.cur.fetchone()[0]:
            if logining:
                self.cur.execute(f"UPDATE casino SET dateLogin = ? WHERE username = ?", (time.ctime(), username))
                self.conn.commit()
                if creatingToken:
                    token = self.creatingTokenDef(id)
                self.logger.debug()
            return True, token
        else:
            return False

    def creatingTokenDef(self, id):
        token = secrets.token_hex(32)
        results = self.tokenCur.execute("SELECT * FROM token WHERE id = ?", (id))
        if results.fetchone() is None:
            self.tokenCur.execute("INSERT INTO token (id, uToken) VALUES (?, ?)", (id, token))
        else:
            self.tokenCur.execute("UPDATE token SET uToken = ? WHERE id = ?", (token, id))
        self.tokenConn.commit()
        return token

    def registration(self, password, username):
        self.cur.execute(f"INSERT INTO casino (username, password, cash, dateReg, dateLogin) VALUES (?, ?, ?, ?, ?)", (username, password, 1000, time.ctime(), time.ctime()))
        self.conn.commit()
        self.logger.debug(f"new user in DB, {username}")

    def changePassword(self, id, oldPassword, newPassword):
        self.cur.execute("SELECT password FROM casino WHERE id = ?", (id))
        if oldPassword == self.cur.fetchone()[0]:
            self.cur.execute("UPDATE casino SET password = ? WHERE id = ?", (newPassword, id))
            self.logger.debug(f"{id} changed password")
        else:
            self.logger.debug(f"{id} the password change has been blocked. Invalid password")
