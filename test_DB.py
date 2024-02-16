import unittest
from database import Database

class TestDB(unittest.TestCase):
    def setUp(self):
        self.db = Database(":memory:")

    def test_changeCash(self):
        # Test initial cash value
        self.db.cur.execute("INSERT INTO casino (username, password, cash, dateReg, dateLogin, muted, banned) VALUES (?, ?, ?, ?, ?, ?, ?)", ("user1", "password1", 1000, "2022-01-01", "2022-01-01", False, False))
        self.db.conn.commit()
        self.db.changeCash("user1", 500)
        self.db.cur.execute("SELECT cash FROM casino WHERE username = ?", ("user1",))
        cash = self.db.cur.fetchone()[0]
        self.assertEqual(cash, 1500)

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


if __name__ == "__main__":
    unittest.main()