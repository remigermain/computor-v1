from .utils import Color, MAX_DEGRES
from .poly import PolyPower, PolyOperande


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

    def verbose(self, info, message):
        if self._verbose:
            print(f"{Color.YELLOW}{info.capitalize()}{Color.WHITE}:\n\t{message}\n")

    def reduce_poly(self, list_poly):
        new_poly = [list_poly[0]]
        last_ope = None
        for poly in list_poly[1:]:
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

    def resolve(self):
        self._before = self.reduce_poly(self._before)
        self._after = self.reduce_poly(self._after)
        self.verbose("reduce degres", self.poly_str(
            self._before) + " = " + self.poly_str(self._after))
