from tkinter import *
from fractions import Fraction

from recur_tensor import RecurTensor
from easy_parser import parse


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class TensorIO(Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.strikes = None
        self.p = 0
        self.q = 0
        self.r = 0
        self.n = 0

    def _next_x(self, x, lvl):
        raise NotImplementedError()

    def _next_y(self, y, lvl):
        raise NotImplementedError()

    def output_tensor(self):
        raise NotImplementedError()

    def get_tensor(self):
        raise NotImplementedError()

    def print(self, lvl, x, y, strikes):
        if lvl == 0:
            strikes.place(x=x, y=y)
            return
        dx = 0
        dy = 0
        if lvl % 2 == 0:
            dx = self._next_x(x, lvl) - x
        else:
            dy = self._next_y(y, lvl) - y

        for i in range(self.n):
            self.print(lvl - 1, x + dx * i, y + dy * i, strikes[i])

    def _destroy(self, strikes, lvl):
        if strikes is None:
            return
        if lvl == 0:
            strikes.destroy()
        else:
            for i in strikes:
                self._destroy(i, lvl - 1)


def read_fraction(entry):
    try:
        return Fraction(entry.get())
    except ValueError:
        return Fraction(0)
    except AttributeError:
        return Fraction(0)


def read_int(entry):
    try:
        return int(entry.get())
    except ValueError:
        return 0
    except AttributeError:
        return 0


class TensorInput(TensorIO):

    def __init__(self, root, point):
        self.WDTH = 5

        self.point = point
        self.p_input = Entry(root, width=self.WDTH)
        self.q_input = Entry(root, width=self.WDTH)
        self.n_input = Entry(root, width=self.WDTH)
        self.readBtn = Button(text="Read", command=self.output_tensor)

        nx = self._next_x(self.point.x, 0)
        nnx = self._next_x(nx, 0)

        self.p_input.place(x=self.point.x, y=self.point.y)
        self.q_input.place(x=nx, y=self.point.y)
        self.n_input.place(x=nnx, y=self.point.y)
        self.readBtn.place(x=self._next_x(nnx, 0), y=self.point.y)

        super().__init__(root)

    def _next_x(self, x, lvl):
        return x + self.WDTH * 5 + (lvl - 1) * lvl * 10

    def _next_y(self, y, lvl):
        return y + lvl * lvl * 8 + 10

    def fill_strikes(self, level):
        if level == 0:
            return Entry(width=self.WDTH)
        return [self.fill_strikes(level - 1) for i in range(self.n)]

    def output_tensor(self):
        super()._destroy(self.strikes, self.r)
        self.p = read_int(self.p_input)
        self.q = read_int(self.q_input)
        self.n = read_int(self.n_input)
        self.r = self.p + self.q
        self.strikes = self.fill_strikes(self.r)
        super().print(self.r, self.point.x, self.point.y + 100, self.strikes)

    def _read_matrix(self, lvl, a, tensor):
        if lvl == 0:
            return tensor.set_data(read_fraction(a))
        else:
            return [self._read_matrix(lvl - 1, a[i], tensor.data[i]) for i in range(self.n)]

    def get_tensor(self):
        tensor = RecurTensor(self.p, self.q, self.n)
        self._read_matrix(self.r, self.strikes, tensor)
        return tensor


class TensorOutput(TensorIO):
    def __init__(self, root, point):
        self._tensor = RecurTensor(0, 0, 0)
        self.point = point
        super().__init__(root)

    def set_tensor(self, tensor):
        self._tensor = tensor

    WDTH = 3

    def _next_x(self, x, lvl):
        return x + self.WDTH * 5 + (lvl - 1) * lvl * 9

    def _next_y(self, y, lvl):
        return y + lvl * lvl * 7 + 10

    def get_tensor(self):
        return self._tensor

    def fill_strikes(self, tensor):
        if tensor.q + tensor.p == 0:
            return Label(text=str(tensor.data))
        return [self.fill_strikes(tensor.data[i]) for i in range(self.n)]

    def output_tensor(self):
        self._destroy(self.strikes, self.r)
        self.p = self._tensor.p
        self.q = self._tensor.q
        self.r = self.p + self.q
        self.n = self._tensor.n
        self.strikes = self.fill_strikes(self._tensor)
        super().print(self.r, self.point.x, self.point.y, self.strikes)


class App(Frame):

    def __init__(self, root):
        self._WDTH = 1220
        self._HGHT = 800
        super().__init__(root)
        root.geometry(str(self._WDTH) + 'x' + str(self._HGHT))
        self._A = TensorInput(root, Point(10, 10))
        self._B = TensorInput(root, Point(610, 10))
        self._ANS = TensorOutput(root, Point(self._WDTH // 2, self._HGHT - 300))

        self._commands = Entry(width=50)
        self._calc = Button(text='Calculate', command=self._run_parser)
        self._build()

    def _build(self):
        self._commands.place(x=50, y=self._HGHT - 200)
        self._calc.place(x=10, y=self._HGHT - 300)

    def _run_parser(self):
        source = self._commands.get()
        values = {
            "A": self._A.get_tensor(),
            "B": self._B.get_tensor()
        }
        self._ANS.set_tensor(parse(source, values.get('A'), values.get('B')))
        # self._parser.parse(source, values))
        self._ANS.output_tensor()


COLOUR = "#F8ECE0"


def main():
    root = Tk()
    root["bg"] = COLOUR
    root.title("Калькулятор")
    app = App(root)
    app.pack()
    root.mainloop()


main()
