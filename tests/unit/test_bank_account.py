# Copyright 2021 Burhanuddin Bhopalwala
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
import pytest

from src.adv import BankAccount
from src.adv import InsufficientAmount
from src.adv import InvalidAmount


@pytest.fixture
def empty_bank_account():
    """Returns empty bank account - balance=0."""
    return BankAccount()


@pytest.fixture
def non_empty_bank_account(amount=100):
    """Returns non empty bank account with default - balance=100."""
    return BankAccount(amount)


def test_default_empty_bank_account(empty_bank_account):
    assert empty_bank_account.balance == 0


def test_non_empty_bank_account(non_empty_bank_account):
    assert non_empty_bank_account.balance == 100


@pytest.mark.skip(reason='Later enable it')
def test_custom_non_empty_bank_account(non_empty_bank_account):
    assert non_empty_bank_account.balance == 200


def test_deposit_empty_bank_account(empty_bank_account):
    empty_bank_account.deposit(150)
    assert empty_bank_account.balance == 150


def test_invalid_deposit_empty_bank_account(empty_bank_account):
    with pytest.raises(InvalidAmount):
        empty_bank_account.deposit(-50)


def test_deposit_non_empty_bank_account(non_empty_bank_account):
    non_empty_bank_account.deposit(150)
    assert non_empty_bank_account.balance == 250


def test_invalid_deposit_non_empty_bank_account(non_empty_bank_account):
    with pytest.raises(InvalidAmount):
        non_empty_bank_account.deposit(-50)


def test_withdraw_non_empty_bank_account(non_empty_bank_account):
    non_empty_bank_account.withdraw(25)
    assert non_empty_bank_account.balance == 75


def test_withdraw_empty_bank_account(empty_bank_account):
    with pytest.raises(InsufficientAmount):
        empty_bank_account.withdraw(150)


def test_invalid_withdraw_empty_bank_account(empty_bank_account):
    with pytest.raises(InvalidAmount):
        empty_bank_account.withdraw(-150)


def test_invalid_withdraw_non_empty_bank_account(non_empty_bank_account):
    with pytest.raises(InvalidAmount):
        non_empty_bank_account.withdraw(-150)


@pytest.mark.parametrize(
    'deposit, withdraw, balance', [(100, 25, 75), (100, 50, 50), (50, 25, 25)]
)
def test_transactions_empty_bank_account(
    empty_bank_account, deposit, withdraw, balance
):
    empty_bank_account.deposit(deposit)
    empty_bank_account.withdraw(withdraw)
    assert empty_bank_account.balance == balance


@pytest.mark.parametrize(
    'deposit, withdraw, balance',
    [(100, 25, 175), (100, 50, 150), (50, 25, 125)],
)
def test_transactions_non_empty_bank_account(
    non_empty_bank_account, deposit, withdraw, balance
):
    non_empty_bank_account.deposit(deposit)
    non_empty_bank_account.withdraw(withdraw)
    assert non_empty_bank_account.balance == balance


def test_count():
    assert BankAccount.count == 16  # * Count of all the above fixtures
