from tkinter import *

from tensor import Tensor


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class TensorInput(Frame):

    def _next(self, x):
        return x + self.WDTH * 10 + 3

    def __init__(self, root, point):
        self.WDTH = 5
        super().__init__(root)
        self.root = root
        self.point = point
        self.p_input = Entry(root, width=self.WDTH)
        self.q_input = Entry(root, width=self.WDTH)
        self.n_input = Entry(root, width=self.WDTH)
        self.p_input.place(x=point.x, y=point.y)
        self.q_input.place(x=self._next(point.x), y=point.y)
        self.n_input.place(x=self._next(self._next(point.x)), y=point.y)
        self.st = Entry()
        self.n = 0
        self.q = 0
        self.p = 0
        self.r = 0
        self.matrix()


    @staticmethod
    def _get(entry):
        try:
            return int(entry.get())
        except ValueError:
            return 0

    def _print(self, lvl, x, y):
        if lvl == 0:
            e = Entry(self.root, width=self.WDTH)
            e.place(x=x, y=y)
            return e
        if lvl % 2 == 1:
            dx = lvl * (self._next(x) - x)
            dy = 0
        else:
            dx = 0
            dy = lvl * 5 + lvl * 8 * lvl

        return [self._print(lvl - 1, x + dx * i, y + dy * i) for i in range(self.n)]

    def _destroy(self, a, lvl):
        if lvl == 0:
            a.destroy()
        else:
            for i in a:
                self._destroy(i, lvl - 1)

    def matrix(self):
        self._destroy(self.st, self.r)
        self.p = self._get(self.p_input)
        self.q = self._get(self.q_input)
        self.n = self._get(self.n_input)
        self.r = self.p + self.q
        self.st = self._print(self.r, self.point.x, self.point.y + 100)

    def _values(self, lvl, a):
        if lvl == 0:
            return self._get(a)
        else:
            return [self._values(lvl - 1, a[i]) for i in range(self.n)]

    def get_tensor(self):
        return Tensor(self.p, self.q, self.n, self._values(self.r, self.st))


class App(Frame):
    def __init__(self, root):
        self.WDTH = 1550
        self.HGHT = 900
        super().__init__(root)
        root.geometry(str(self.WDTH) + 'x' + str(self.HGHT))
        self.A = TensorInput(root, Point(10, 10))
        self.B = TensorInput(root, Point(775, 10))
        self.read = Button(text="read")
        self.read.config(command=self._call_read)
        self.read.place(x=1000, y=50)
        self._build()

    def _call_read(self):
        self.A.matrix()
        self.B.matrix()

    def _build(self):
        pass


def main():
    root = Tk()
    root["bg"] = "#F8ECE0"
    root.title("Калькулятор")
    root.resizable(False, False)
    app = App(root)
    app.pack()
    root.mainloop()


main()
