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

    def __add__(self, other):
        assert self.p == other.p and self.q == other.q and self.n == other.n
        t = Tensor(self.p, self.q, self.n)
        t.a = self._recur_add(self.a, other.a, self.r)
        return t
