# # Implementation of the Polynomial ADT using a sorted linked list.


class Polynomial:
    """
    Class for Polynomial representation.
    """
    # Create a new polynomial object.

    def __init__(self, degree=None, coefficient=None):
        """
        Initializes a Polynomial with following parameters:
        :param degree: int
        :param coefficient: float
        """
        if degree is None:
            self._polyHead = None
        else:
            self._polyHead = _PolyTermNode(degree, coefficient)
        self._polyTail = self._polyHead

    # Return the degree of the polynomial.
    def degree(self):
        """
        Returns a degree of a polynomial.
        :return: int
        """
        if self._polyHead is None:
            return -1
        else:
            return self._polyHead.degree

    # Return the coefficient for the term of the given degree.
    def __getitem__(self, degree):
        """
        Returns a coefficient of a term with given degree.
        :param degree: int
        :return: int
        """
        assert self.degree() >= 0, "Operation not permitted on an empty polynomial."
        curNode = self._polyHead
        while curNode is not None and curNode.degree > degree:
            curNode = curNode.next

        if curNode is None or curNode.degree != degree:
            return 0.0
        else:
            return curNode.coefficient

    # Evaluate the polynomial at the given scalar value.
    def evaluate(self, scalar):
        """
        Returns a calculated polynomial.
        :param scalar: float
        :return: Polynomial
        """
        assert self.degree() >= 0, "Only non -empty polynomials can be evaluated."
        result = 0.0
        curNode = self._polyHead
        while curNode is not None:
            result += curNode.coefficient * (scalar ** curNode.degree)
            curNode = curNode.next
        return result

    # Polynomial addition: newPoly = self + rhsPoly.
    def __add__(self, rhsPoly):
        """
        Adds two polynomials.
        :param rhsPoly: Polynimial (polynomial that is being added).
        :return: Polynomial (summ polynomial).
        """
        return self.simple_add(rhsPoly)

    # Polynomial subtraction: newPoly = self - rhsPoly.
    def __sub__(self, rhsPoly):
        """
        Subtracts two polynomials.
        :param rhsPoly: Polynimial (polynomial that is being added).
        :return: Polynomial (subtraction polynomial).
        """
        return self.simple_add(rhsPoly, True)

    # Polynomial multiplication: newPoly = self * rhsPoly.
    def __mul__(self, rhsPoly):
        """
        Multiplies two polynomials.
        :param rhsPoly: Polynimial (polynomial that is being added).
        :return: Polynomial (multiply polynomial).
        """
        newPoly = Polynomial(0, 0)
        curNode_1 = self._polyHead
        while curNode_1:
            curNode_2 = rhsPoly._polyHead
            while curNode_2:
                new_degree = curNode_1.degree + curNode_2.degree
                new_coeff = curNode_1.coefficient * curNode_2.coefficient
                newPoly = newPoly + Polynomial(new_degree, new_coeff)
                curNode_2 = curNode_2.next
            curNode_1 = curNode_1.next
        return newPoly

    def simple_add(self, rhsPoly, neg=False):
        """
        Adds two polynomials.
        :param rhsPoly: Polynimial (polynomial that is being added).
        :param neg: bool (addition or subtraction).
        """
        newPoly = Polynomial()
        if self.degree() > rhsPoly.degree():
            maxDegree = self.degree()
        else:
            maxDegree = rhsPoly.degree()

        i = maxDegree
        while i >= 0:
            if neg == False:
                value = self[i] + rhsPoly[i]
            else:
                value = self[i] - rhsPoly[i]
            # print(self[i], rhsPoly[i])
            newPoly._appendTerm(i, value)
            i -= 1
        return newPoly

    def _appendTerm(self, new_degree, new_coeff):
        """
        Adds a term to a polynomial in correct place.
        :param new_degree: int
        :param new_coeff: float
        """
        assert new_degree >= 0, "Only non -empty terms can be added."
        curNode = self._polyHead
        if not curNode:
            self._polyHead = _PolyTermNode(new_degree, new_coeff)
        else:
            if self.degree() < new_degree:
                newNode = _PolyTermNode(new_degree, new_coeff)
                newNode.next = self._polyHead
                self._polyHead = newNode
            else:
                while curNode.next is not None:
                    if curNode.next.degree < new_degree:
                        break
                    curNode = curNode.next
                newNode = _PolyTermNode(new_degree, new_coeff)
                newNode.next = curNode.next
                curNode.next = newNode

    def __str__(self):
        """
        Returns a string representation of a polynomial.
        :return: srt
        """
        str_repr = ""
        cur_node = self._polyHead

        while cur_node:
            if cur_node.coefficient:
                str_repr += str(cur_node) + " + "
            cur_node = cur_node.next

        return str_repr[:-2]

# Class for creating polynomial term nodes used with the linked list.


class _PolyTermNode(object):
    """
    Class for polynomial node representation.
    """

    def __init__(self, degree, coefficient):
        """
        Initializes a node with following parameters:
        :param degree: int
        :param coefficient: float
        :param next: _PolyTermNode
        """
        self.degree = degree
        self.coefficient = coefficient
        self.next = None

    def __str__(self):
        """
        Prints the value stored in self.
        __str__: Node -> Str
        """
        return str(self.coefficient) + "*x^" + str(int(self.degree))


if __name__ == "__main__":

    # a = Polynomial(1, 3)
    # a._appendTerm(3, 5)
    # a._appendTerm(2, 7)
    # a._appendTerm(0, 9)
    # b = Polynomial(2, 4)
    # f = Polynomial(3, 6)

    # c = a+b
    # d = c-f
    # k = a*f

    # print(a)
    # print(c)
    # print(d)
    # print(k)
