# Copyright 2021 Burhanuddin Bhopalwala
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# import os
import logging
from collections import Counter
from functools import reduce
from itertools import accumulate
from itertools import zip_longest
from operator import mul
from pprint import pformat

# from dotenv import load_dotenv()

handler = 'advanced_python'
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(handler)

# * python-dotenv - load_dotenv() demo
# load_dotenv()
# ENV = os.getenviron("ENV", "dev")
# logger.info("## ENV loaded using python-dotenv: %s", ENV)


def factorial(n):
    """Apply cumulatively to the items of the iterables."""
    return reduce(mul, range(1, n + 1), 1)


logger.info('## Reduce factorial %s', factorial(5))


def mul_acumulate(numbers):
    """Same as reduce but return the intermediate results."""
    results = accumulate(numbers, mul)
    for step in results:
        print(step)


numbers = [1, 2, 3, 4, 5]
mul_acumulate(numbers)


invitees = [
    {'email': 'alex@example.com', 'name': 'Alex', 'status': 'attending'},
    {'email': 'brian@example.com', 'name': 'Brian', 'status': 'declined'},
    {'email': 'carol@example.com', 'name': 'Carol', 'status': 'pending'},
    {'email': 'david@example.com', 'name': 'David', 'status': 'attending'},
    {'email': 'maria@example.com', 'name': 'Maria', 'status': 'attending'},
]


def transform_invitees(invitees):
    """Transform invitees data using reduce & accumulate."""

    def transform_data(acc, invitee):
        acc[invitee['email']] = invitee['status']
        return acc

    results = reduce(transform_data, invitees, {})
    return results


logger.info('## Transform %s', pformat(transform_invitees(invitees)))

# * Counting elements from iterables


def get_counts(fruits):
    results = {}
    counts = Counter(fruits)
    # * Use key, value for kwargs
    for fruit, count in counts.items():
        results[count] = results.get(count, []) + [fruit]
    return results


fruits = ['apple', 'apple', 'apple', 'watermelon', 'grapes', 'grapes']
logger.info('## Counter %s', get_counts(fruits))


def find_anagrams(word, list_of_words):
    """AI is creating summary for find_anagrams

    Args:
        word (str): [description]
        list_of_words (lis): [description]

    Returns:
        (list): [description]
    """
    sorted_word = sorted(word)
    return list(filter(lambda w: sorted(w) == sorted_word, list_of_words))


def xor(a1s, b1s):
    """A map() demo (use instead of loops for new list generation from existing on a per element basis).

    Args:
        a1s (list): [description]
        b1s (list): [description]

    Returns:
        (list): XOR list
    """
    a1s_b1s = zip_longest(a1s, b1s, fillvalue=0)
    return list(map(lambda t: t[0] ^ t[1], a1s_b1s))


def enumerate_demo(numbers=[1, 2, 3]):
    """An enumerate demo.

    Args:
        numbers (list, optional): [description]. Defaults to [1, 2, 3].
    """
    for index, element in enumerate(numbers):
        print(f'index: {index}, value: {element}')


enumerate_demo()

# * lambda arguments:expressions
# * Annonymous functions & created at runtime!
# multiplication = lambda a,b,c: a*b*c
# multiplication(1, 2, 3)

fruits = {'apples': 50, 'bananas': 10}


def sorted_key(fruits):
    """A sorted() demo - using custom key.

    Args:
        fruits (list): [description]
    """
    return sorted(fruits, key=lambda fruit: fruit[-2])


logger.info('## sorted() demo %s', sorted_key(fruits))


def number_seen(list_of_numbers):
    """A set() - demo.

    Args:
        list_of_numbers (list): [description]

    Returns:
        result (list): [description]
    """
    # result = []
    # n_set = set()
    # for number in list_of_numbers:
    #     try:
    #         n_set.remove(number)
    #         result.append("YES")
    #         n_set.add(number)
    #     except KeyError:
    #         n_set.add(number)
    #         result.append("NO")
    #         continue
    result = []
    result_set = set()
    for x in list_of_numbers:
        if x not in result_set:
            result_set.add(x)
            result.append('NO')
        else:
            result.append('YES')
    return result


logger.info('## set() demo: %s', number_seen([1, 2, 1, 2, 4, 5]))


def complement(universal_set, A):
    """A set() demo - complement of a set.

    Args:
        universal_set ([type]): [description]
        A ([type]): [description]

    Returns:
        (bool): [description]
    """
    if universal_set.issuperset(A):
        return universal_set.difference(A)
    return None


# * https://github.com/DavidArmendariz/advanced-python-skills-course/blob/master/notebooks/24_frozenset.ipynbß
