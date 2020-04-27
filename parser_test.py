from parser import Parser
from tensor import Tensor


def main():
	p = Parser()
	print((Tensor(0, 0, 0, 5) + Tensor(0 ,0 ,0, 1)).a)
	print(p.parse("222", dict()).a)
	print(p.parse("3+1", dict()).a)
	print(p.parse(" 3 - 1 ", dict()).a)
	print(p.parse(" A + B - 3 + 5 - 3 + (-2)", { "A" : Tensor(0, 0, 0, 1), "B" : Tensor(0, 0, 0 , 2)}).a)


main()
