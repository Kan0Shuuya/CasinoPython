import sqlite3
import time
import secrets
from loguru import logger as lg

#Я ненавижу писать запросы LMAO, т.к у нас нет никакого способа проверить работоспособность модуля, т.к нет самого казино.
#Завтра, я буду тестить скрипт в консоси. так что код модуля БД у нас есть, а вот работает ли он вообще яхз.
#P.S: Хотел выебнуться и написать на английском комент, но решил не портить тебе зрение своим английским. По этому испорчу тебе его мои русским
#P.P.S: Тяжело жить без подствеки ошибок в словах KEkw
class DB:
    def __init__(self, fileName:str):
        self.conn = sqlite3.connect(fileName)
        self.cur = self.conn.cursor()
        self.tokenConn = sqlite3.connect(":memory:")
        self.tokenCur = self.tokenConn.cursor()

        self.logger = lg

        self.cur.execute("""CREATE TABLE IF NOT EXISTS casino (
        username TEXT PRIMARY KEY,
        password TEXT,
        cash INTEGER,
        dateReg TEXT,
        dateLogin TEXT,    
        muted BOOLEAN,
        banned BOOLEAN
        )""")
        self.tokenCur.execute("""CREATE TABLE IF NOT EXISTS token (
        username TEXT PRIMARY KEY,
        uToken TEXT
        )""")
        self.conn.commit()
        self.tokenConn.commit()

    def changeCash(self, username, deltaCash):
        self.cur.execute("SELECT cash FROM casino WHERE username = ?", (username,))
        result = self.cur.fetchone()[0]
        result += deltaCash
        self.cur.execute(f"UPDATE casino SET cash = ? WHERE username = ?", (result, username))
        self.conn.commit()

    def loginingWithPassword(self, username, password, creatingToken=False) -> list:
        self.cur.execute("SELECT password FROM casino WHERE username = ?", (username,))
        if password == self.cur.fetchone()[0]:
            self.cur.execute(f"UPDATE casino SET dateLogin = ? WHERE username = ?", (time.ctime(), username))
            self.conn.commit()
            if creatingToken:
                return [True, self.creatingTokenDef(username)]
        else:
            return [False, None]

    @lg.catch
    def creatingTokenDef(self, username):
        token = secrets.token_hex(32)
        results = self.tokenCur.execute("SELECT * FROM token WHERE username = ?", (username,))
        if results.fetchone() is None:
            self.tokenCur.execute("INSERT INTO token (username, uToken) VALUES (?, ?)", (username, token))
        else:
            self.tokenCur.execute("UPDATE token SET uToken = ? WHERE username = ?", (token, username))
        self.tokenConn.commit()
        return token

    def registration(self, username, password):
        self.cur.execute("SELECT username FROM casino WHERE username = ?", (username,))
        if self.cur.fetchone() is not None:
            return False

        self.cur.execute(f"INSERT INTO casino (username, password, cash, dateReg, dateLogin, muted, banned) VALUES (?, ?, ?, ?, ?, ?, ?)", (username, password, 1000, time.ctime(), time.ctime(), False, False))
        self.conn.commit()
        self.logger.debug(f"new user in DB, {username}")
        return True

    def changePassword(self, username, oldPassword, newPassword):
        self.cur.execute("SELECT password FROM casino WHERE username = ?", (username,))
        res = self.cur.fetchone()[0]
        if oldPassword == res:
            self.cur.execute("UPDATE casino SET password = ? WHERE username = ?", (newPassword, username))
            self.conn.commit()
            self.logger.debug(f"{username} changed password")
            return True
        else:
            self.logger.debug(f"{username} the password change has been blocked. Invalid password")
            return False

    def printTokenDB(self):
        self.tokenCur.execute("SELECT * FROM token")
        self.logger.debug(self.tokenCur.fetchall())

    def printDB(self):
        self.cur.execute("SELECT * FROM casino")
        self.logger.debug(self.cur.fetchall())
