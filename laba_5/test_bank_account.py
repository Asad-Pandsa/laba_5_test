import unittest

from bank_account import BankAccount


class TestBankAccount(unittest.TestCase):
    def setUp(self):
        self.account = BankAccount("Анна Иванова", "123456")

    def test_new_account_stores_details_and_starts_empty(self):
        self.assertEqual(self.account.owner_name, "Анна Иванова")
        self.assertEqual(self.account.account_number, "123456")
        self.assertEqual(self.account.get_balance(), 0)
        self.assertTrue(self.account.is_empty())

    def test_account_requires_owner_and_account_number(self):
        with self.assertRaises(ValueError):
            BankAccount("", "123456")
        with self.assertRaises(ValueError):
            BankAccount("Анна Иванова", " ")

    def test_deposit_increases_balance(self):
        self.account.deposit(250)

        self.assertEqual(self.account.get_balance(), 250)
        self.assertFalse(self.account.is_empty())

    def test_deposit_rejects_invalid_amount_without_changing_balance(self):
        for amount in (0, -10, float("nan"), float("inf")):
            with self.subTest(amount=amount):
                with self.assertRaises(ValueError):
                    self.account.deposit(amount)
                self.assertEqual(self.account.get_balance(), 0)

        for amount in ("10", None, True):
            with self.subTest(amount=amount):
                with self.assertRaises(TypeError):
                    self.account.deposit(amount)
                self.assertEqual(self.account.get_balance(), 0)

    def test_withdraw_decreases_balance(self):
        self.account.deposit(300)

        self.account.withdraw(125)

        self.assertEqual(self.account.get_balance(), 175)

    def test_withdraw_rejects_invalid_or_excessive_amount(self):
        self.account.deposit(100)

        for amount in (0, -10, 101):
            with self.subTest(amount=amount):
                with self.assertRaises(ValueError):
                    self.account.withdraw(amount)
                self.assertEqual(self.account.get_balance(), 100)

        with self.assertRaises(TypeError):
            self.account.withdraw("10")
        self.assertEqual(self.account.get_balance(), 100)

    def test_transfer_moves_same_amount_between_accounts(self):
        recipient = BankAccount("Иван Петров", "654321")
        self.account.deposit(500)

        self.account.transfer_to(recipient, 175)

        self.assertEqual(self.account.get_balance(), 325)
        self.assertEqual(recipient.get_balance(), 175)

    def test_failed_transfer_does_not_change_either_account(self):
        recipient = BankAccount("Иван Петров", "654321")
        self.account.deposit(100)
        recipient.deposit(20)

        with self.assertRaises(ValueError):
            self.account.transfer_to(recipient, 101)

        self.assertEqual(self.account.get_balance(), 100)
        self.assertEqual(recipient.get_balance(), 20)

    def test_transfer_rejects_invalid_recipient_or_same_account(self):
        self.account.deposit(100)

        with self.assertRaises(TypeError):
            self.account.transfer_to(object(), 10)
        with self.assertRaises(ValueError):
            self.account.transfer_to(self.account, 10)

        self.assertEqual(self.account.get_balance(), 100)

    def test_account_becomes_empty_after_full_withdrawal(self):
        self.account.deposit(75)
        self.account.withdraw(75)

        self.assertEqual(self.account.get_balance(), 0)
        self.assertTrue(self.account.is_empty())


if __name__ == "__main__":
    unittest.main()