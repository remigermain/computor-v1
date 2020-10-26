from .utils import DEFAULT_INDEFINITE


class Poly:
    is_operande = False
    is_power = False

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self)


class PolyOperande(Poly):
    is_operande = True

    def is_plus(self):
        return self.value == "+"

    def __repr__(self):
        return "(plus)" if self.is_plus() else "(minus)"


class PolyPower(Poly):
    is_power = True

    def __init__(self, value, num, degres, indefinite=DEFAULT_INDEFINITE):
        self.value = value
        self.num = num
        self.degres = degres
        self.indefinite = indefinite

    def __str__(self):
        return f"{self.num} * {self.indefinite}^{self.degres}"
