import sqlite3
import time
from loguru import logger as lg


class DB:
    def __init__(self, fileName: str):
        self.conn = sqlite3.connect(fileName, check_same_thread=False)
        self.cur = self.conn.cursor()

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
        self.conn.commit()

    def changeCash(self, username, deltaCash):
        self.cur.execute("SELECT cash FROM casino WHERE username = ?", (username,))
        result = self.cur.fetchone()[0]
        result += deltaCash
        self.cur.execute(f"UPDATE casino SET cash = ? WHERE username = ?", (result, username))
        self.conn.commit()

    def registration(self, username, password):
        self.cur.execute("SELECT username FROM casino WHERE username = ?", (username,))
        if self.cur.fetchone() is not None:
            return False

        self.cur.execute(
            f"INSERT INTO casino (username, password, cash, dateReg, dateLogin, muted, banned) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (username, password, 1000, time.ctime(), time.ctime(), False, False))
        self.conn.commit()
        self.logger.debug(f"new user in DB, {username}")
        return True

    def getPassword(self, username: str) -> str | None:
        self.cur.execute("SELECT password FROM casino WHERE username = ?", (username,))
        result = self.cur.fetchone()
        if not result:
            return None
        return result

    def getAllUserDataAsDict(self, username: str) -> dict | None:
        self.cur.execute("SELECT * FROM casino WHERE username = ?", (username,))
        result = self.cur.fetchone()
        if not result:
            return None
        columns = [description[0] for description in self.cur.description]
        data = dict(zip(columns, result))
        return data

    def getNonSensitiveUserDataAsDict(self, username: str) -> dict | None:
        self.cur.execute("SELECT username, cash, dateReg, dateLogin, muted, banned FROM casino WHERE username = ?",
                         (username,))
        result = self.cur.fetchone()
        if not result:
            return None
        columns = [description[0] for description in self.cur.description]
        data = dict(zip(columns, result))
        return data

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
