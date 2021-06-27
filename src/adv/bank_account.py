# Copyright 2021 Burhanuddin Bhopalwala
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""This is Bank Account module.

Author: Burhanuddin Bhopalwala
Last Modified On: 15/Apr/2021
Last Modified By: Burhanuddin Bhopalwala
"""


class InvalidAmount(Exception):
    pass


class InsufficientAmount(Exception):
    pass


class BankAccount(object):
    count = 0  # * Static member - attribute

    def __init__(self, initial_amount=0, min_amount=10) -> None:
        self._balance = initial_amount  # * Public member - attribute
        self.__min_balance = min_amount  # * Private member - attribute

        BankAccount.count += 1
        return None

    def __str__(self) -> str:
        return 'A BankAccount'

    # * Allows some form of data encapsulation (private/public).

    @property
    def balance(self) -> int:
        return self._balance

    @balance.setter
    def balance(self, amount: int) -> None:
        if self.__is_invalid_amount(amount):
            raise InvalidAmount('Invalid amount.')
        self._balance = amount
        return None

    # * Private member - method
    def __is_invalid_amount(self, amount: int) -> bool:
        if isinstance(amount, int) and amount >= self.__min_balance:
            return False
        return True

    def deposit(self, amount: int) -> None:
        if (self.__is_invalid_amount(amount)) or (amount == 0):
            raise InvalidAmount('Invalid deposit amount.')
        self.balance += amount

    def withdraw(self, amount: int) -> None:
        if self.__is_invalid_amount(amount):
            raise InvalidAmount('Invalid withdraw amount.')
        if self.balance < amount:
            raise InsufficientAmount('Insufficient amount.')
        self.balance -= amount
        return None

    @staticmethod  # * Class helper/utility`
    def get_count() -> int:
        return BankAccount.count

    def __del__(self):
        BankAccount.count -= 1
