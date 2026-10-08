import math


class BankAccount:
    def __init__(self, owner_name, account_number):
        if not isinstance(owner_name, str) or not owner_name.strip():
            raise ValueError("Имя владельца должно быть непустой строкой")
        if not isinstance(account_number, str) or not account_number.strip():
            raise ValueError("Номер счёта должен быть непустой строкой")

        self._owner_name = owner_name
        self._account_number = account_number
        self._balance = 0

    @property
    def owner_name(self):
        return self._owner_name

    @property
    def account_number(self):
        return self._account_number

    def _validate_amount(self, amount):
        if isinstance(amount, bool) or not isinstance(amount, (int, float)):
            raise TypeError("Сумма должна быть числом")
        if not math.isfinite(amount):
            raise ValueError("Сумма должна быть конечным числом")
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")

    def deposit(self, amount):
        self._validate_amount(amount)
        self._balance += amount

    def withdraw(self, amount):
        self._validate_amount(amount)
        if amount > self._balance:
            raise ValueError("Недостаточно средств на счёте")
        self._balance -= amount

    def transfer_to(self, recipient, amount):
        if not isinstance(recipient, BankAccount):
            raise TypeError("Получатель должен быть банковским счётом")
        if recipient is self:
            raise ValueError("Нельзя перевести деньги на тот же счёт")

        self._validate_amount(amount)
        if amount > self._balance:
            raise ValueError("Недостаточно средств на счёте")

        self._balance -= amount
        recipient._balance += amount

    def get_balance(self):
        return self._balance

    def is_empty(self):
        return self._balance == 0