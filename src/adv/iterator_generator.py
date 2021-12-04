# Copyright 2021 Burhanuddin Bhopalwala
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# *  https://github.com/DavidArmendariz/advanced-python-skills-course/blob/master/notebooks/08_iterators.ipynb
# * Implementing python for loop (using iterators)...
fruits = ['apples', 'bananas', 'mangoes']
iterator_fruits = iter(fruits)
while True:
    try:
        current_element = next(iterator_fruits)
        print(current_element)
    except StopIteration:
        break

# """
#     Iterables vs Iterators

#     * So far we have used these two words a lot, and maybe I have use it interchangeably.
#     But, there is a suttle difference.

#     * An iterable is a representation of a series of elements that can be iterated over.
#     It does not have any iteration state such as a "current element". But every iterable
#     can be converted to an iterator by using iter(). Typically, an iterable can produce any number of valid iterators.

#     * An iterator is the object with iteration state. It lets you check if it has more elements
#     using the next() or __next__() and move to the next element (if any).
# """


class PowersOfTwo:
    def __init__(self, maximum=0):
        self.maximum = maximum

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n <= self.maximum:
            result = 2 ** self.n
            self.n += 1
            return result
        else:
            raise StopIteration


obj = iter(PowersOfTwo(5))
next(obj)  # 1, 2, 4, 8, 16
# ---------------------------------------------------------------------------
# StopIteration                             Traceback (most recent call last)
# <ipython-input-37-2e36627a780e> in <module>
# ----> 1 next(obj)

# * Generators!
# * They are a simple way of creating iterators. All the work we have done is handled by generators.
# * They are easy to implement: we just have to create a function that returns elements with yield instead of return.
# * They can contain one or more yield statements.
# * When called, it returns an object (iterator) but does not start execution immediately.
# * Once the function yields, the function is paused and the control is transferred to the caller.
# * Local variables and their states are remembered between successive calls.

# * https://github.com/DavidArmendariz/advanced-python-skills-course/blob/master/notebooks/09_generators.ipynb
# * https://github.com/DavidArmendariz/advanced-python-skills-course/blob/master/solutions/solution_prime_numbers.ipynb


def fibonacci_numbers():
    a = 0
    b = 1
    yield a
    yield b
    while 1:
        c = a + b
        a, b = b, c
        yield c


def prime_numbers():
    n = 2
    yield (2)
    while True:
        n += 1
        is_prime = True
        for i in range(2, n):
            if n % i == 0:
                is_prime = False
        if is_prime:
            yield (n)
