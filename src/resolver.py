from .utils import Color, MAX_DEGRES
from .eq import Power, Operande
from .poly import get_poly_class


# '\u221A1\u03056\u0305'

class Resolver:

    def __init__(self, data, verbose=False):
        self._before = data[0]
        self._after = data[1]
        self._verbose = verbose
        self.verbose("normalize equation",
                     self.poly_str(self._before) + " = " +
                     self.poly_str(self._after)
                     )

    def __str__(self):
        return " ".join(str(d) for d in self._before)

    def poly_str(self, poly_list):
        return " ".join(str(d) for d in poly_list)

    def verbose(self, info, message, force=False):
        if self._verbose or force:
            print(f"{Color.YELLOW}{info.capitalize()}{Color.WHITE}:\n\t{message}\n")

    def _reduce(self):
        new_after = [
            obj
            if obj.is_power else
            Operande("-" if obj.is_plus() else "-")
            for obj in self._after
        ]
        self._before.extend([Operande("-"), *new_after])

        self.verbose("merge equation", self.poly_str(self._before) + " = 0")

        new_poly = [self._before[0]]
        last_ope = None
        for poly in self._before[1:]:
            if poly.is_operande:
                last_ope = poly
            else:
                f = list(filter(lambda x: x.is_power and x.degres ==
                                poly.degres, new_poly))
                if not f:
                    new_poly.extend([last_ope, poly])
                else:
                    if last_ope.is_plus():
                        f[0].num += poly.num
                    else:
                        f[0].num -= poly.num
        return new_poly

    def remove_poly(self, lst):
        """
            remove all poly with zero
        """
        new_lst = []

        last = None
        for nxt in lst:
            if nxt.is_operande:
                last = nxt
            elif nxt.num != 0:
                if not last:
                    new_lst.append(nxt)
                else:
                    new_lst.extend([last, nxt])
        if len(new_lst) == 0:
            return [Power("0", 0.0, 0)]
        return new_lst

    def find_degres(self, lst):
        _max = 0
        for el in lst:
            if el.is_power and el.degres > _max:
                _max = el.degres
        return _max

    def resolve(self):
        lst = self._reduce()
        self.verbose("pre-reduce equation", self.poly_str(lst) + " = 0")

        lst = self.remove_poly(lst)

        self.verbose("reduce equation", self.poly_str(
            lst) + " = 0", force=True)

        degres = self.find_degres(lst)
        self.verbose("Polynomial degree", degres, force=True)

        poly = get_poly_class(degres)(lst, verbose=self._verbose)
        poly.resolve()
