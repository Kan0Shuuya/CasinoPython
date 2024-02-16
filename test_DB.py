import unittest
from unittest.mock import MagicMock
from DB import DB

class TestDB(unittest.TestCase):
    def setUp(self):
        self.db = DB(":memory:", MagicMock())

    def test_changeCash(self):
        # Test initial cash value
        self.db.cur.execute("INSERT INTO casino (username, password, cash, dateReg, dateLogin, muted, banned) VALUES (?, ?, ?, ?, ?, ?, ?)", ("user1", "password1", 1000, "2022-01-01", "2022-01-01", False, False))
        self.db.conn.commit()
        self.db.changeCash("user1", 500)
        self.db.cur.execute("SELECT cash FROM casino WHERE username = ?", ("user1",))
        cash = self.db.cur.fetchone()[0]
        self.assertEqual(cash, 1500)

    def test_loginingWithPassword(self):
        # Test successful login
        self.db.cur.execute("INSERT INTO casino (username, password, cash, dateReg, dateLogin, muted, banned) VALUES (?, ?, ?, ?, ?, ?, ?)", ("user1", "password1", 1000, "2022-01-01", "2022-01-01", False, False))
        self.db.conn.commit()
        result = self.db.loginingWithPassword("user1", "password1", True)
        self.assertTrue(result[0])
        self.assertIsInstance(result[1], str)

        # Test unsuccessful login
        result = self.db.loginingWithPassword("user1", "wrongpassword", True)
        self.assertFalse(result[0])
        self.assertIsNone(result[1])

    def test_creatingTokenDef(self):
        # Test creating token for new user
        result = self.db.creatingTokenDef("user1")
        self.assertIsNotNone(result)

        # Test updating token for existing user
        result2 = self.db.creatingTokenDef("user1")
        self.assertIsNotNone(result2)
        self.assertNotEqual(result, result2)

    def test_registration(self):
        # Test successful registration
        result = self.db.registration("user1", "password1")
        self.assertTrue(result)

        # Test registration with existing username
        result2 = self.db.registration("user1", "password2")
        self.assertFalse(result2)

    def test_changePassword(self):
        # Test successful password change
        self.db.cur.execute("INSERT INTO casino (username, password, cash, dateReg, dateLogin, muted, banned) VALUES (?, ?, ?, ?, ?, ?, ?)", ("user1", "password1", 1000, "2022-01-01", "2022-01-01", False, False))
        self.db.conn.commit()
        result = self.db.changePassword("user1", "password1", "newpassword")
        self.assertTrue(result)

        # Test password change with invalid old password
        result2 = self.db.changePassword("user1", "wrongpassword", "newpassword")
        self.assertFalse(result2)

    def test_printTokenDB(self):
        # Test printing token database
        self.db.tokenCur.execute("INSERT INTO token (username, uToken) VALUES (?, ?)", ("user1", "token1"))
        self.db.tokenConn.commit()
        self.db.printTokenDB()  # Check console output for token database

    def test_printDB(self):
        # Test printing casino database
        self.db.cur.execute("INSERT INTO casino (username, password, cash, dateReg, dateLogin, muted, banned) VALUES (?, ?, ?, ?, ?, ?, ?)", ("user1", "password1", 1000, "2022-01-01", "2022-01-01", False, False))
        self.db.conn.commit()
        self.db.printDB()  # Check console output for casino database

if __name__ == "__main__":
    unittest.main()