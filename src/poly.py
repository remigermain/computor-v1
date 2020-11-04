from .utils import Color


class Poly:

    def __init__(self, data, verbose=False, no_print=False):
        self.data = data
        self._verbose = verbose
        self._no_print = no_print

    def verbose(self, info, message, force=False):
        if (self._verbose or force) and not self._no_print:
            print(f"{Color.YELLOW}{info.capitalize()}{Color.WHITE}:\n\t{message}\n")

    def verbose_force(self, info, message):
        self.verbose(info, message, force=True)

    def print(self, *args):
        if not self._no_print:
            print(*args)

    def only_result(self, *args):
        if self._no_print:
            print(*args)

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
    """
        poly for degres 0
    """

    def resolve(self):
        # TODO
        if not self._no_print:
            print("\tall solution are possible.")
        else:
            print("NO")


class Poly1(Poly):
    """
        poly for degres 1
    """

    def resolve(self):
        a = self.get_poly_degres(1)
        b = self.get_poly_degres(0)

        solution = -b / a
        self.verbose(
            "calculate",
            f"a = {a}\n\tb = {b}\n\n\t"
            f"x\u00B9 = (-b / a) = ({-b} / {a})\n\tx\u00B9 = {solution}"
        )
        self.print(f"\tsolution is \u2A10 = {solution}")


class Poly2(Poly):
    """
        poly for degres 2
    """

    def calcul_delta(self, a, b, c):
        return (b * b) - 4 * a * c

    def delta_negative(self, delta):
        self.verbose_force("result",
                           f"delta is lower than 0 ({ delta }), no solution possible."
                           )
        self.print("\tx = \u2205")
        self.only_result("NO")

    def delta_zero(self, a, b, c):
        self.verbose_force("result", "delta is 0, only one solution")
        self.print(f"\tx\u2070 =  -b  / ( 2 x a ) = {-b} / ( 2 x {a} ) ")
        solution = -b / (2 * a) if a != 0 else 0
        self.print(f"\n\tsolution is \u2A10 = {solution}")
        self.only_result(solution)

    def delta_positive(self, delta, a, b, c):
        self.verbose_force(
            "result", "delta is upper than 0, you have 2 solution")
        delta_sq = self.sqrt(delta)

        eq = "\tx{res} = (-b {sign} \u221A\u0394) / (2 x a) = ({b} {sign} \u221A{delta}) / (2 x {a})"
        data = {
            'a': a,
            'b': b,
            'c': c,
            'delta': delta
        }

        # X1, first solution
        self.print(eq.format(sign="-", res="\u00B9", ** data))
        x1 = (-b - delta_sq) / (2 * a) if a != 0 else 0
        self.print(f"\tx\u00B9 = {x1}\n")

        # X2, second solution
        self.print(eq.format(sign="+", res="\u00B2", ** data))
        x2 = (-b + delta_sq) / (2 * a) if a != 0 else 0
        self.print(f"\tx\u00B2 = {x2}\n")

        # resume solution
        self.print("\n\tsolution is \u2A10{ " + f"{x1} ; {x2}" + " }")
        self.only_result(x1)
        self.only_result(x2)

    def resolve(self):
        a = self.get_poly_degres(2)
        b = self.get_poly_degres(1)
        c = self.get_poly_degres(0)

        delta = self.calcul_delta(a, b, c)
        veb = f"a = {a}\n\tb = {b}\n\tc = {c}\n\n\t"
        veb += f"\u0394 delta = (b\u00B2 - 4) * a * c = ({b}\u00B2 - 4) * {a} * {c}\n\t\u0394 delta = {delta}"
        self.verbose("calculate delta", veb)

        # call respective solution
        if delta < 0:
            self.delta_negative(delta)
        elif delta == 0:
            self.delta_zero(a, b, c)
        else:
            self.delta_positive(delta, a, b, c)


def get_poly_class(degres): return eval(f"Poly{degres}")
