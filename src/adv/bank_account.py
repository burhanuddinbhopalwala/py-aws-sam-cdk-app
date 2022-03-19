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
    COUNT = 0  # * Static member # Class variable - attribute

    def __init__(self, initial_amount=0, min_amount=10) -> None:
        self._balance = initial_amount  # * Public member - attribute
        self.__min_balance = min_amount  # * Private member - attribute

        BankAccount.COUNT += 1
        return None

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
        return BankAccount.COUNT

    # def __dir__(self) -> list:
    #     class_consts = ['COUNT']
    #     private_attrs = ['__min_balance']
    #     public_attrs = ['_balance']
    #     class_methods = []
    #     static_methods = ['get_count']
    #     private_methods = ['__is_invalid_amount']
    #     public_methods = ['deposit', 'withdraw']
    #     class_members = class_consts + private_attrs + public_attrs + \
    #         class_methods + static_methods + private_methods + public_methods
    #     return class_members

    def __repr__(self) -> str:
        return f'BankAccount(initial_amount={self.balance}, min_amount={self.__min_balance})'

    def __str__(self) -> str:
        return f'BankAccount with initial_amount {self.name} and min_amount is {self.__min_balance})'

    def __del__(self):
        BankAccount.COUNT -= 1
        # * NOTE: Python has automatic garbage collector!
