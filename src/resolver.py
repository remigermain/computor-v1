from .utils import Color, MAX_DEGRES, DEFAULT_INDEFINITE
from .eq import Power, Operande
from .poly import get_poly_class


class Resolver:

    _valid = None

    def __init__(self, data, verbose=False, no_print=False, indefinite=DEFAULT_INDEFINITE):
        self._first_data = data[0]
        self._second_data = data[1]
        self._verbose = verbose
        self._no_print = no_print
        self._ind = indefinite
        self.verbose("normalize equation",
                     self.poly_str(self._first_data) + " = " +
                     self.poly_str(self._second_data)
                     )

    def __str__(self):
        return " ".join(str(d) for d in self._first_data)

    def poly_str(self, poly_list):
        return " ".join(str(d) for d in poly_list)

    def verbose(self, info, message, force=False):
        if (self._verbose or force) and not self._no_print:
            print(f"{Color.YELLOW}{info.capitalize()}{Color.WHITE}:\n\t{message}\n")

    def _reduce(self):
        new_second_data = [
            obj
            if obj.is_power else
            Operande("-" if obj.is_plus() else "-")
            for obj in self._second_data
        ]
        self._first_data.extend([Operande("-"), *new_second_data])

        self.verbose("merge equation", self.poly_str(
            self._first_data) + " = 0")

        new_poly = [self._first_data[0]]
        last_ope = None
        for poly in self._first_data[1:]:
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

        if len(lst) == 1:
            return lst

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
            return [Power(0, 0, indefinite=self._ind)]
        return new_lst

    def find_degres(self, lst):
        _max = 0
        for el in lst:
            if el.is_power and el.degres > _max:
                _max = el.degres
        return _max

    def resolve(self):
        self._final_reduce = self._reduce()
        self.verbose(
            "pre-reduce equation",
            self.poly_str(self._final_reduce) + " = 0"
        )

        self._final_reduce = self.remove_poly(self._final_reduce)

        self.verbose(
            "reduce equation",
            self.poly_str(self._final_reduce) + " = 0",
            force=True
        )
        # check degres
        self._max_degres = self.find_degres(self._final_reduce)
        self.verbose("Polynomial degree", self._max_degres, force=True)

    def generate_result(self):
        poly = get_poly_class(self._max_degres)(
            self._final_reduce, verbose=self._verbose, no_print=self._no_print)
        return poly.resolve()
