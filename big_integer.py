class BigIntegerADT:
    """Class that represents big integers."""

    def __init__(self, initvalue="0"):
        """Initializes a big integer."""
        if initvalue[0] == '-':
            self._sign = 0
            self.initvalue = initvalue[1:][::-1]
        else:
            self._sign = 1
            self.initvalue = initvalue[::-1]
        self._head = Digit(self.initvalue[0])
        curDigit = self._head
        for digit in self.initvalue[1:]:
            curDigit.next = Digit(digit)
            temp = curDigit
            curDigit = curDigit.next
            curDigit.prev = temp
        self._rear = curDigit

    def __len__(self) -> int:
        """Returns the length of an integer."""
        length = 1
        curDigit = self._head
        while curDigit:
            length += 1
            curDigit = curDigit.next
        return length

    def __getitem__(self, index: int) -> int:
        """Returns a value of a digit at given position."""
        iter_index = 0
        curNode = self._head
        while (curNode is not None) and (iter_index < index):
            curNode = curNode.next
            iter_index += 1

        if curNode is None:
            return 0.0
        else:
            return curNode.value

    def __eq__(self, other) -> bool:
        """Returns bool of (self == other)."""
        if self._sign != other._sign:
            return False
        if len(self) != len(other):
            return False
        curDigit1 = self._rear
        curDigit2 = other._rear
        while curDigit1:
            if curDigit1.value != curDigit2.value:
                return False
            curDigit1 = curDigit1.prev
            curDigit2 = curDigit2.prev
        else:
            return True

    def __ne__(self, other) -> bool:
        """Returns bool of (self != other)."""
        if self == other:
            return False
        else:
            return True

    def __gt__(self, other) -> bool:
        """Returns bool of (self > other)."""
        if self._sign > other._sign:
            return True
        if self._sign < other._sign:
            return False
        if self == other:
            return False
        max_len = max(len(self), len(other))
        if self._sign == 1:
            for i in range(max_len - 2, -1, -1):
                if self[i] > other[i]:
                    return True
                else:
                    return False
        else:
            temp1, temp2 = self._sign, other._sign
            self._sign, other._sign = 1, 1
            if self > other:
                return False
            else:
                return True
            self._sign, other._sign = temp1, temp2

    def __ge__(self, other) -> bool:
        """Returns bool of (self >= other)."""
        if self > other or self == other:
            return True
        else:
            return False

    def __lt__(self, other) -> bool:
        """Returns bool of (self < other)."""
        if self >= other:
            return False
        else:
            return True

    def __le__(self, other) -> bool:
        """Returns bool of (self <= other)."""
        if self < other or self == other:
            return True
        else:
            return False

    def __add__(self, other):
        """Returns sum of two integers."""
        resultInt = BigIntegerADT()
        extra = 0
        max_ind = max(len(self), len(other))
        if self.mod_gt(other):
            max_sign = self._sign
        else:
            max_sign = other._sign
        if self._sign == other._sign:
            for i in range(max_ind):
                if extra:
                    sum_dig = self[i] + other[i] + extra
                else:
                    sum_dig = self[i] + other[i]
                extra, value = divmod(sum_dig, 10)
                resultInt.value = value
                resultInt._appenDigit(value)
        else:
            if self.mod_gt(other):
                for i in range(max_ind):
                    if extra:
                        sum_dig = self[i] - other[i] + extra
                    else:
                        sum_dig = self[i] - other[i]
                    extra, value = divmod(sum_dig, 10)
                    resultInt.value = value
                    resultInt._appenDigit(value)
            else:
                for i in range(max_ind):
                    if extra:
                        sum_dig = other[i] - self[i] + extra
                    else:
                        sum_dig = other[i] - self[i]
                    extra, value = divmod(sum_dig, 10)
                    resultInt.value = value
                    resultInt._appenDigit(value)

        resultInt._head = resultInt._head.next
        resultInt._sign = max_sign
        resultInt.eraseZero()
        return resultInt

    def __sub__(self, other):
        """Returns subtraction of two integers."""
        other._sign = 1 - other._sign
        resultInt = self + other
        return resultInt

    def oneDigigMul(self, digit):
        """Returns a result of multiplication if integer and one digit."""
        resultInt = BigIntegerADT()
        extra = 0
        for i in range(len(self)):
            if extra:
                sum_dig = self[i] * digit + extra
            else:
                sum_dig = self[i] * digit
            extra, value = divmod(sum_dig, 10)
            resultInt.value = value
            resultInt._appenDigit(value)
        return resultInt

    def __mul__(self, other):
        """Returns multiplication of two integers."""
        if self._sign == other._sign:
            res_sign = 1
        else:
            res_sign = 0
        result = 0
        if len(self) < len(other):
            for i in range(len(self)):
                result += other.oneDigigMul(self[i]).int_repr()*(10**i)
        else:
            for i in range(len(other)):
                result += self.oneDigigMul(other[i]).int_repr()*(10**i)
        resultInt = BigIntegerADT(str(result))
        resultInt._head = resultInt._head.next
        resultInt._sign = res_sign
        return resultInt

    def __floordiv__(self, other):
        """Returns floor division of two integers."""
        result = 0
        temp1 = self._sign
        temp2 = other._sign
        self._sign = 1
        other._sign = 1
        newBigInt = other
        while newBigInt <= self:
            newBigInt = newBigInt + other
            a = newBigInt.int_repr()
            result += 1
        if temp1 != temp2:
            result *= -1
            result -= 1
        self._sign = temp1
        other._sign = temp2
        return result

    def __mod__(self, other):
        """Returns mod dividion of two integers."""
        self_int = self.int_repr()
        other_int = other.int_repr()
        if self._sign == other._sign == 1:
            res = self_int - other_int*(self // other)
        elif self._sign > other._sign:
            res = self_int + other_int*(self // other)
        elif self._sign < other._sign:
            res = -self_int - other_int*(self // other)
        else:
            res = -self_int - other_int*(self // other)
            res *= -1
        return res

    def __pow__(self, other):
        """Returns power of two integers."""
        power = other.int_repr()
        newBigInt = self
        for i in range(power):
            newBigInt = newBigInt * self
        return newBigInt

    def int_repr(self):
        """Returns an int representation of a big integer."""
        curDigit = self._head
        i = 1
        result = 0
        while curDigit:
            result += curDigit.value * i
            i *= 10
            curDigit = curDigit.next
        return result

    def eraseZero(self):
        """Deletes zeros from the back of the big integer."""
        curDigit = self._rear
        while curDigit.value == 0:
            curDigit = curDigit.prev
            curDigit.next = None
            self._rear = curDigit

    def _appenDigit(self, value):
        """Adds a digit to a big integer."""
        curDigit = self._head
        while curDigit.next:
            curDigit = curDigit.next
        curDigit.next = Digit(value)
        curDigit.next.prev = curDigit
        self._rear = curDigit.next

    def mod_gt(self, other):
        """Returns bool of absolute value comparison."""
        temp1 = self._sign
        temp2 = other._sign
        self._sign = 1
        other._sign = 1
        res = self > other
        self._sign = temp1
        other._sign = temp2
        return res

    def __str__(self) -> str:
        """Returns a string representation of big integer."""
        curDigit = self._head
        st = ''
        while curDigit:
            st += str(curDigit.value)
            curDigit = curDigit.next
        if self._sign == 0:
            return '-' + st[::-1]
        else:
            return st[::-1]


class Digit:
    """Class that represents digits."""

    def __init__(self, value=None):
        """Initializes a digit."""
        if value is not None:
            self.value = int(value)
        else:
            self.value = None
        self.next = None
        self.prev = None

    def __str__(self):
        """Returns a string representation of a digit."""
        return str(self.value)
