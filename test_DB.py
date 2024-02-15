import unittest
from unittest.mock import MagicMock
from DB import DB
from loguru import logger

class TestDB(unittest.TestCase):
    def setUp(self):
        self.logger = MagicMock()
        self.db = DB(":memory:", logger)

    def test_changeCash(self):
        # Test initial cash value
        self.db.cur.execute("INSERT INTO casino (id, cash) VALUES (?, ?)", (1, 100))
        self.db.changeCash(1, 50)
        self.db.cur.execute("SELECT cash FROM casino WHERE id = ?", (1,))
        cash = self.db.cur.fetchone()[0]
        self.assertEqual(cash, 150)

    def test_Logining(self):
        # Test successful login
        self.db.cur.execute("INSERT INTO casino (id, username, password) VALUES (?, ?, ?)", (1, "user1", "password1"))
        result, token = self.db.Logining("user1", "password1", logining=True, creatingToken=True)
        self.assertTrue(result)
        self.assertIsNotNone(token)

        # Test failed login
        result, token = self.db.Logining("user1", "wrong_password")
        self.assertFalse(result)
        self.assertIsNone(token)

    def test_creatingTokenDef(self):
        # Test creating a new token
        self.db.tokenCur.execute("INSERT INTO token (id, uToken) VALUES (?, ?)", (1, "token1"))
        token = self.db.creatingTokenDef(1)
        self.assertNotEqual(token, "token1")

        # Test updating an existing token
        self.db.tokenCur.execute("INSERT INTO token (id, uToken) VALUES (?, ?)", (2, "token2"))
        token = self.db.creatingTokenDef(2)
        self.assertNotEqual(token, "token2")

    def test_registration(self):
        # Test registration
        self.db.registration("password1", "user1")
        self.db.cur.execute("SELECT username FROM casino WHERE username = ?", ("user1",))
        username = self.db.cur.fetchone()[0]
        self.assertEqual(username, "user1")

    def test_changePassword(self):
        # Test changing password with valid old password
        self.db.cur.execute("INSERT INTO casino (id, password) VALUES (?, ?)", (1, "old_password"))
        self.db.changePassword(1, "old_password", "new_password")
        self.db.cur.execute("SELECT password FROM casino WHERE id = ?", (1,))
        password = self.db.cur.fetchone()[0]
        self.assertEqual(password, "new_password")

        # Test changing password with invalid old password
        self.db.cur.execute("INSERT INTO casino (id, password) VALUES (?, ?)", (2, "old_password"))
        self.db.changePassword(2, "wrong_password", "new_password")
        self.db.cur.execute("SELECT password FROM casino WHERE id = ?", (2,))
        password = self.db.cur.fetchone()[0]
        self.assertEqual(password, "old_password")

if __name__ == "__main__":
    unittest.main()