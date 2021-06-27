# Copyright 2021 Burhanuddin Bhopalwala
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
import pytest

from src.adv.bank_account import BankAccount
from src.adv.bank_account import InsufficientAmount
from src.adv.bank_account import InvalidAmount

# * fixtures outside class is more relevant for scope = 'class'.
# * But still below shims with scope = 'function' works.
# @pytest.fixture(scope="function", autouse=True)
# def empty_bank_account(request):
#     """Returns empty bank account - balance=0."""
#     request.cls.empty_bank_account = BankAccount()
#     yield
#     # self.tear_down()
#     del request.cls.empty_bank_account


# @pytest.fixture(scope="function", autouse=True)
# def non_empty_bank_account(request, amount=100):
#     """Returns non empty bank account with default - balance=100."""
#     request.cls.non_empty_bank_account = BankAccount(amount)
#     yield
#     # self.tear_down()
#     del request.cls.non_empty_bank_account


# @pytest.mark.usefixtures("empty_bank_account")
# @pytest.mark.usefixtures("non_empty_bank_account")
class TestBankAccount(object):
    """
        Ref 1: https://betterprogramming.pub/understand-5-scopes-of-pytest-fixtures-1b607b5c19ed
        Ref 2: https://www.lambdatest.com/blog/end-to-end-tutorial-for-pytest-fixtures-with-examples/
    """

    @pytest.fixture(scope='function', autouse=True)
    def empty_bank_account(self):
        """Returns empty bank account - balance=0."""
        self.empty_bank_account = BankAccount()
        yield
        # self.tear_down()
        del self.empty_bank_account

    @pytest.fixture(scope='function', autouse=True)
    def non_empty_bank_account(self, amount=100):
        """Returns non empty bank account with default - balance=100."""
        self.non_empty_bank_account = BankAccount(amount)
        yield
        # self.tear_down()
        del self.non_empty_bank_account

    def test_default_empty_bank_account(self):
        assert self.empty_bank_account.balance == 0

    @pytest.mark.xfail(reason='Learning xfail')
    def test_non_empty_bank_account(self):
        assert self.non_empty_bank_account.balance == 100

    @pytest.mark.skip(reason='Learning skip')
    def test_custom_non_empty_bank_account(self):
        assert self.non_empty_bank_account.balance == 200

    def test_deposit_empty_bank_account(self):
        self.empty_bank_account.deposit(150)
        assert self.empty_bank_account.balance == 150

    @pytest.mark.bank_account_skipif
    @pytest.mark.skipif(True, reason='Test skipif')
    def test_invalid_deposit_empty_bank_account(self):
        with pytest.raises(InvalidAmount):
            self.empty_bank_account.deposit(-50)

    def test_deposit_non_empty_bank_account(self):
        self.non_empty_bank_account.deposit(150)
        assert self.non_empty_bank_account.balance == 250

    def test_invalid_deposit_non_empty_bank_account(self):
        with pytest.raises(InvalidAmount):
            self.non_empty_bank_account.deposit(-50)

    def test_withdraw_non_empty_bank_account(self):
        self.non_empty_bank_account.withdraw(25)
        assert self.non_empty_bank_account.balance == 75

    def test_withdraw_empty_bank_account(self):
        with pytest.raises(InsufficientAmount):
            self.empty_bank_account.withdraw(150)

    def test_invalid_withdraw_empty_bank_account(self):
        with pytest.raises(InvalidAmount):
            self.empty_bank_account.withdraw(-150)

    def test_invalid_withdraw_non_empty_bank_account(self):
        with pytest.raises(InvalidAmount):
            self.non_empty_bank_account.withdraw(-150)

    @pytest.mark.parametrize(
        'deposit, withdraw, balance', [
            (100, 25, 75), (100, 50, 50), (50, 25, 25)]
    )
    def test_transactions_empty_bank_account(
        self, deposit, withdraw, balance
    ):
        self.empty_bank_account.deposit(deposit)
        self.empty_bank_account.withdraw(withdraw)
        assert self.empty_bank_account.balance == balance

    @pytest.mark.parametrize(
        'deposit, withdraw, balance',
        [(100, 25, 175), (100, 50, 150), (50, 25, 125)],
    )
    def test_transactions_non_empty_bank_account(
        self, deposit, withdraw, balance
    ):
        self.non_empty_bank_account.deposit(deposit)
        self.non_empty_bank_account.withdraw(withdraw)
        assert self.non_empty_bank_account.balance == balance

    def test_static_count(self):
        # * count is 2 (2 fixtrues) for this test not yet tear_down
        assert BankAccount.count == 2


# * pytest --markers
# * pytest --fixtures
