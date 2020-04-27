from itertools import permutations

class Tensor:
    def build(self, r):
        if r == 0:
            return 0
        else:
            return [self.build(r - 1) for i in range(self.n)]

    # p from V
    # q from V*
    # n --- dimension
    def __init__(self, p, q, n, a=None):
        self.p = p
        self.q = q
        self.r = p + q
        self.n = n
        self.a = (self.build(self.r) if a is None else a)

    def _recur_add(self, a, b, lvl):
        if lvl == 0:
            return a + b
        c = [0] * len(a)
        for i in range(len(a)):
            c[i] = self._recur_add(a[i], b[i], lvl - 1)
        return c

    def _recur_neg(self, a, lvl):
        if lvl == 0:
            return -a
        ans = [0] * len(a)
        for i in range(len(a)):
            ans[i] = self._recur_neg(a[i], lvl - 1)
        return ans

    def __add__(self, other):
        assert self.p == other.p and self.q == other.q and self.n == other.n
        t = Tensor(self.p, self.q, self.n)
        t.a = self._recur_add(self.a, other.a, self.r)
        return t

    def __neg__(self):
        return Tensor(self.p, self.q, self.n, self._recur_neg(self.a, self.r))

    def __sub__(self, other):
        return self + (-other)

    # p1 q1  p2 q2
    # 
    def _read(self, a, ind, i = 0):
        if i == len(ind):
            return a
        else:
            return self._read(a[ind[-i - 1]], ind, i + 1)

    def _write(self, a, ind, i, value):
        if i == len(ind) - 1:
            a[ind[-i - 1]] = value
        else:
            self._write(a[ind[-i - 1]], ind, i + 1, value)

    def _build(self, lvl):
        if lvl == 0:
            return 0
        return [self._build(lvl - 1) for i in range(self.n)]

    def _recur_mul(self, a, b, p1, p2, q1, q2, ind, ans):
        for i in permutations(ind[: p1]):
            for j in permutations(ind[p1 : p2 + p1]):
                for k in permutations(ind[p2 + p1 : q1 + p2 + p1]):
                    for l in permutations(ind[q1 + p2 + p1 :]):
                        self._write(self._read(self._read(self._read(ans, l), k), j), i, 0, self._read(self._read(a, k), i) * self._read(self._read(b, l), j))


    def __mul__(self, other):
        assert self.n == other.n
        p1 = self.p
        p2 = other.p
        q1 = self.q
        q2 = other.q
        ind = list(range(p1)) + list(range(p1, p2 + p1)) + list(range(p2 + p1, p2 + p1 + q1)) + list(range(p2 + p1 + q1, p2 + p1 + q1 + q2))
        ans = self._build(self.r + other.r)
        self._recur_mul(self.a, other.a, self.p, other.p, self.q, other.q, ind, ans)
        return ans
