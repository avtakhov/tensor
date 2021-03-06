from copy import deepcopy
from itertools import permutations
from math import factorial
from fractions import Fraction


def count(perm):
    ans = 0
    for i in range(len(perm)):
        for j in range(i + 1, len(perm)):
            if perm[j] < perm[i]:
                ans += 1
    return ans


class RecurTensor:
    def __init__(self, p, q, n):
        self.p = p
        self.q = q
        self.n = n
        if p + q == 0:
            self.data = 0
        else:
            nq = q
            np = p
            if q > 0:
                nq -= 1
            else:
                np -= 1
            self.data = [RecurTensor(np, nq, n) for i in range(n)]

    def set_data(self, data):
        self.data = data

    def get_scalar(self, ind):
        if self.p + self.q == 0:
            return self
        else:
            t = ind.pop()
            ans = self.data[t].get_scalar(ind)
            ind.append(t)
            return ans

    def write(self, ind, value):
        t = self.get_scalar(ind)
        t.data = value

    def read(self, ind):
        t = self.get_scalar(ind)
        return t.data

    def __add__(self, other):
        assert self.n == other.n
        ans = RecurTensor(self.p, self.q, self.n)
        if self.p + self.q == 0:
            ans.set_data(self.data + other.data)
        else:
            ans.set_data([self.data[i] + other.data[i] for i in range(self.n)])
        return ans

    def __sub__(self, other):
        assert self.n == other.n
        ans = RecurTensor(self.p, self.q, self.n)
        if self.p + self.q == 0:
            ans.set_data(self.data - other.data)
        else:
            ans.set_data([self.data[i] - other.data[i] for i in range(self.n)])
        return ans

    def __neg__(self):
        ans = RecurTensor(self.p, self.q, self.n)
        if self.p + self.q == 0:
            ans.set_data(-self.data)
        else:
            ans.set_data([-self.data[i] for i in range(self.n)])
        return ans

    def coo(self, t):
        if t == 0:
            return [[]]
        ans = []
        prev = self.coo(t - 1)
        for arr in prev:
            for i in range(self.n):
                arr0 = deepcopy(arr)
                arr0.append(i)
                ans.append(arr0)
        return ans

    def __mul__(self, other):
        ans = RecurTensor(self.p + other.p, self.q + other.q, self.n)
        for i in self.coo(self.p):
            for j in other.coo(other.p):
                for k in self.coo(self.q):
                    for l in other.coo(other.q):
                        ind = i + j + k + l
                        value = self.read(i + k) * other.read(j + l)
                        ans.write(ind, value)
        return ans

    def transpose(self, arg, permutation):
        permutation = list(map(lambda x: x - 1, permutation))
        ans = RecurTensor(self.p, self.q, self.n)
        for i in self.coo(self.p):
            for j in self.coo(self.q):
                if arg == 0:
                    ind = [0] * self.p
                    for x in range(self.p):
                        ind[x] = i[permutation[x]]
                    ind = ind + j
                elif arg == 1:
                    ind = [0] * self.q
                    for x in range(self.q):
                        ind[x] = j[permutation[x]]
                    ind = i + ind
                else:
                    ind = -1
                ans.write(i + j, self.read(ind))

        return ans

    def __xor__(self, other):
        one = RecurTensor(0, 0, self.n)
        e = self * other
        one.set_data(
            Fraction(factorial(self.p + other.p), factorial(self.p) * factorial(other.p)) * Fraction(1, factorial(e.p)))
        ans = RecurTensor(e.p, e.q, e.n)
        for i in permutations(list(range(1, e.p + 1))):
            if count(i) % 2 == 0:
                ans += e.transpose(0, i)
            else:
                ans -= e.transpose(0, i)
        return one * ans
