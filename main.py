from tkinter import *

from tensor import Tensor
from parser import Parser


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class TensorIO(Frame):
    def __init__(self, root, point):
        super().__init__(root)
        self.root = root
        self.st = self._get_simple()
        self.p = 0
        self.q = 0
        self.r = 0
        self.n = 0
        self.output_tensor()

    def _get_st(self):
        return self.st

    def _set_st(self, st):
        self.st = st
    
    def _get_simple(self, element=0):
        raise NotImplementedError()

    def _next_x(self, x, lvl):
        raise NotImplementedError()

    def _next_y(self, y, lvl):
        raise NotImplementedError()

    def output_tensor():
        raise NotImplementedError()

    def get_tensor():
        raise NotImplementedError()

    def _build_array(self, lvl):
        if lvl == 0:
            return 0
        return [self._build_array(lvl - 1) for i in range(self.n)]

    def _print(self, lvl, x, y, a):
        if lvl == 0:
            e = self._get_simple(a)
            e.place(x=x, y=y)
            return e
        if lvl % 2 == 1:
            dx = self._next_x(x, lvl) - x
            dy = 0
        else:
            dx = 0
            dy = self._next_y(y, lvl) - y

        return [self._print(lvl - 1, x + dx * i, y + dy * i, a[i]) for i in range(self.n)]

    def _destroy(self, a, lvl):
        if lvl == 0:
            a.destroy()
        else:
            for i in a:
                self._destroy(i, lvl - 1)



class TensorInput(TensorIO):

    def __init__(self, root, point):
        self.WDTH = 5

        self.point = point
        self.p_input = Entry(root, width=self.WDTH)
        self.q_input = Entry(root, width=self.WDTH)
        self.n_input = Entry(root, width=self.WDTH)
        self.readBtn = Button(text="Read",command=self.output_tensor)


        nx = self._next_x(self.point.x, 0)
        nnx = self._next_x(nx, 0)
        
        self.p_input.place(x=self.point.x, y=self.point.y)
        self.q_input.place(x=nx, y=self.point.y)
        self.n_input.place(x=nnx, y=self.point.y)
        self.readBtn.place(x=self._next_x(nnx, 0), y=self.point.y)

        super().__init__(root, point)


    def _next_x(self, x, lvl):
        # return x + self.WDTH * 5 + lvl * lvl * 12
        return x + self.WDTH * 5 + lvl * lvl * 12

    def _next_y(self, y, lvl):
        # return y + (lvl - 1) * lvl * 7 + 10
        return y + (lvl - 1) * lvl * 7 + 10

    @staticmethod
    def _get(entry):
        try:
            return int(entry.get())
        except ValueError:
            return 0

    def _get_simple(self, element=0):
        return Entry(width=self.WDTH)

    def output_tensor(self):
        self._destroy(super()._get_st(), self.r)
        self.p = self._get(self.p_input)
        self.q = self._get(self.q_input)
        self.n = self._get(self.n_input)
        self.r = self.p + self.q
        arr = super()._build_array(self.r);
        super()._set_st(self._print(self.r, self.point.x, self.point.y + 100, arr))

    def _read_matrix(self, lvl, a):
        if lvl == 0:
            return self._get(a)
        else:
            return [self._read_matrix(lvl - 1, a[i]) for i in range(self.n)]

    def get_tensor(self):
        return Tensor(self.p, self.q, self.n, self._read_matrix(self.r, self.st))



class TensorOutput(TensorIO):
    def __init__(self, root, point):
        self._tensor = Tensor(0, 0, 0, 0)
        self.point = point
        super().__init__(root, point)

    def set_tensor(self, tensor):
        self._tensor = tensor

    WDTH = 7

    def _next_x(self, x, lvl):
        return x + self.WDTH * 5 + lvl * lvl * 12

    def _next_y(self, y, lvl):
        return y + (lvl - 1) * lvl * 5 + 10

    def _get_simple(self, element=0):
        return Label(width=TensorOutput.WDTH,text=str(element))

    def get_tensor(self):
        return self._tensor

    def output_tensor(self):
        self._destroy(super()._get_st(), self.r)
        self.p = self.get_tensor().p
        self.q = self.get_tensor().q
        self.r = self.get_tensor().r
        self.n = self.get_tensor().n
        super()._set_st(self._print(self.r, self.point.x, self.point.y, self.get_tensor().a))


class App(Frame): 

    def __init__(self, root):
        self._WDTH = 1220
        self._HGHT = 800
        super().__init__(root)
        root.geometry(str(self._WDTH) + 'x' + str(self._HGHT))
        self._A = TensorInput(root, Point(10, 10))
        self._B = TensorInput(root, Point(610, 10))
        self._ANS = TensorOutput(root, Point(self._WDTH//2, self._HGHT-300))
        self._parser = Parser()

        self._commands = Entry(width=50)
        self._calc = Button(text='Calculate', command=self._run_parser)
        self._build()

    def _build(self):
        self._commands.place(x=50,y=self._HGHT-200)
        self._calc.place(x=10,y=self._HGHT-300)

    def _run_parser(self):
        source = self._commands.get()
        values = {
            "A" : self._A.get_tensor(),
            "B" : self._B.get_tensor()
        }
        self._ANS.set_tensor(self._parser.parse(source, values))
        self._ANS.output_tensor()

COLOUR = "#F8ECE0"

def main():
    root = Tk()
    root["bg"] = COLOUR 
    root.title("Калькулятор")
    root.resizable(False, False)
    app = App(root)
    app.pack()
    root.mainloop()


main()
