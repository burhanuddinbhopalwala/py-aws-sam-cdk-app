# Copyright 2021 Burhanuddin Bhopalwala
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# """
#     Python closures
#     * There are 3 things that we need in order to have a closure:
#         * We must have a nested function.
#         * The enclosing function must return the nested function.
#         * The nested function must refer to a argument(s) defined in the enclosing function.
# """


def print_message(message):
    def printer():
        # nonlocal message
        # message += "World!" #* UnboundLocalError
        print(message)

    return printer


another_function = print_message('Hello')
another_function()  # Hello
del print_message
another_function()  # Hello

# """
#     When to use closures?
#     * Decorators!
#     * Data hiding. Thus, allows us to avoid the use of global values.
#     * It can also provide an OO solution to the problem (Classes with one function usually).
# """


class Multiplier:
    def __init__(self, n):
        self.n = n

    def multiply(self, x):
        return x * self.n


obj = Multiplier(5)
obj.multiply(7)  # 35


def multiplier(n):
    def multiply(x):
        return x * n

    return multiply


multiplier_by_5 = multiplier(5)
multiplier_by_5(7)  # 35
