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

    def get_num_degres(self, degres) -> float:
        last = None
        for poly in self.data:
            if poly.is_operande:
                last = poly
            elif poly.degres == degres:
                num = -1 if last and not last.is_plus() else 1
                return poly.num * num
        return 0.0

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
        b = self.get_num_degres(0)
        if b == 0:
            self.print("\tall solution are possible.")
            return "ALL"
        else:
            self.print("\the have no solution.")
            return "NO"


class Poly1(Poly):
    """
        poly for degres 1
    """

    def resolve(self):
        a = self.get_num_degres(1)
        b = self.get_num_degres(0)

        solution = -b / a if a != 0 else "ALL"
        self.verbose(
            "calculate",
            f"\ta = {a}\n"
            f"\tb = {b}\n\n"
            "\tx\u00B9 = (-b / a)\n"
            f"\tx\u00B9 = ({-b} / {a})\n"
            f"\tx\u00B9 = {solution}"
        )
        if a != 0:
            self.print(f"\tsolution is \u2A10 = {solution}")
        else:
            self.print("\tall solution are possible.")
        return solution


class Poly2(Poly):
    """
        poly for degres 2
    """

    def calcul_delta(self, a, b, c):
        delta = (b * b) - 4 * a * c
        veb = f"a = {a}\n\tb = {b}\n\tc = {c}\n\n" \
              f"\t\u0394 = (b\u00B2 - 4) * a * c\n" \
              f"\t\u0394 = ({b}\u00B2 - 4) * {a} * {c}\n" \
              f"\t\u0394 = {delta}"
        self.verbose("calculate delta", veb)
        return delta

    def delta_negative(self, delta, a, b, c):
        self.verbose_force("result",
                           f"delta is lower than 0 ({ delta }), no solution possible."
                           )
        self.print("\tx = \u2205")
        return "NO"

    def delta_zero(self, a, b, c):
        self.verbose_force("result", "delta is 0, only one solution")
        solution = -b / (2 * a) if a != 0 else 0
        self.print(
            f"\tx\u2070 = -b / ( 2 * a )\n"
            f"\tx\u2070 = {-b} / ( 2 * {a} )\n"
            f"\tx\u2070 = {solution}"
        )
        self.print(f"\n\tsolution is \u2A10 = {solution}")
        return solution

    def delta_positive(self, delta, a, b, c):
        self.verbose_force(
            "result", "delta is upper than 0, you have 2 solution")
        delta_sq = self.sqrt(delta)

        eq = "\tx{res} = (-b {sign} \u221A\u0394) / (2 * a)\n"\
             "\tx{res} = ({b} {sign} \u221A{delta}) / (2 * {a})"

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
        return [x1, x2]

    def resolve(self):
        a = self.get_num_degres(2)
        b = self.get_num_degres(1)
        c = self.get_num_degres(0)

        delta = self.calcul_delta(a, b, c)

        # call respective solution
        if delta < 0:
            return self.delta_negative(delta, a, b, c)
        elif delta == 0:
            return self.delta_zero(a, b, c)
        else:
            return self.delta_positive(delta, a, b, c)


def get_poly_class(degres): return eval(f"Poly{degres}")
