from .utils import Color


class Poly:

    def __init__(self, data, verbose=False):
        self.data = data
        self._verbose = verbose

    def verbose(self, info, message, force=False):
        if self._verbose or force:
            print(f"{Color.YELLOW}{info.capitalize()}{Color.WHITE}:\n\t{message}\n")

    def print(self, info, message):
        self.verbose(info, message, force=True)

    def get_poly_degres(self, degres):
        last = None
        for poly in self.data:
            if poly.is_operande:
                last = poly
            elif poly.degres == degres:
                if last and not last.is_plus():
                    num = -1
                else:
                    num = 1
                return poly.num * num
        return 0

    def sqrt(self, num):
        n = 1
        for _ in range(10):
            n = (n + num / n) * 0.5
        return n

    def resolve(self):
        assert not "you need to implement this method"


class Poly0(Poly):
    def resolve(self):
        print("all solution is possible")


class Poly1(Poly):
    pass


class Poly2(Poly):

    def delta(self, a, b, c):
        return (b * b) - 4 * a * c

    def resolve(self):
        a = self.get_poly_degres(2)
        b = self.get_poly_degres(1)
        c = self.get_poly_degres(0)

        self.verbose("data in equation", f"a = {a}, b = {b}, c = {c}")

        delta = self.delta(a, b, c)
        veb = f"b\u00B2 - 4 * 4 * c = {b}\u00B2  - 4 * {a} * {c} = {delta}\n\t\u0394 delta = {delta}"
        self.verbose("calculate delta", veb)

        if delta < 0:
            self.print("result", "delta is lower than 0, no solution")
            print("\tx = \u2205")

        elif delta == 0:
            self.print("result", "delta is 0, only one solution")

            print(f"\tx\u2070 =  -b  / ( 2 x a ) = {-b} / ( 2 x {a} ) ")
            solution = -b / (2 * a)
            print(f"solution is {solution}")

        else:
            sol = []
            self.print("result", "delta is upper than 0, you have 2 solution")
            delta_sq = self.sqrt(delta)

            print(
                f"\tx\u00B9 = ( -b - \u221A\u0394 ) / ( 2 x a ) = ( {-b} - \u221A{delta} ) / ( 2 x {a} ) ")
            solution = (-b - delta_sq) / (2 * a)
            sol.append(str(solution))
            print(f"\tx\u00B9 = {solution}\n")

            print(
                f"\tx\u00B2 = ( -b + \u221A\u0394 ) / ( 2 x a ) = ( {-b} - \u221A{delta} ) / ( 2 x {a} ) ")
            solution = (-b + delta_sq) / (2 * a)
            sol.append(str(solution))
            print(f"\tx\u00B2 = {solution}")

            sol = " ; ".join(sol)
            print("\n\tsolution is \u2A10{ " + sol + " }")


def get_poly_class(degres):
    return eval(f"Poly{degres}")
