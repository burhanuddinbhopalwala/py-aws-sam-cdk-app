# Copyright 2021 Burhanuddin Bhopalwala
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# * https: // www.geeksforgeeks.org/extend-class-method-in-python/
# * definition of superclass "Triangles"


class Triangles(object):

    count = 0

    def __init__(self, name, s1, s2, s3):
        self.name = name
        self.s1 = s1
        self.s2 = s2
        self.s3 = s3
        Triangles.count += 1

    def setName(self, name):
        self.name = name

    def setdim(self, s1, s2, s3):
        self.s1 = s1
        self.s2 = s2
        self.s3 = s3

    def getcount(self):
        return Triangles.count

    # * superclass's version of display()
    def display(self):
        return (
            'Name: '
            + self.name
            + '\nDimensions: '
            + str(self.s1)
            + ', '
            + str(self.s2)
            + ', '
            + str(self.s3)
        )


# * definition of the subclass
# * inherits from "Triangles"


class Peri(Triangles):

    def __init__(self):
        super().__init__()

    def calculate(self):
        self.pm = 0
        self.pm = self.s1 + self.s2 + self.s3

    # * extended method
    def display(self):

        # * calls display() of superclass
        print(super(Peri, self).display())

        # * adding its own properties
        return self.pm


def main():

    # * instance of the subclass
    p = Peri('PQR', 2, 3, 4)

    # * call to calculate
    p.calculate()

    # * one call is enough
    print(p.display())


main()
