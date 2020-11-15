from .utils import DEFAULT_INDEFINITE


class Eq:
    is_operator = False
    is_power = False

    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self)


class Operator(Eq):
    is_operator = True

    def __init__(self, value):
        super().__init__(value)
        self._is_plus = None

    def is_plus(self):
        if self._is_plus is None:
            self._is_plus = self.value in ["+"]
        return self._is_plus

    def __repr__(self):
        return "(plus)" if self.is_plus() else "(minus)"


class Power(Eq):
    is_power = True

    def __init__(self, num: float, degres: int, indefinite=DEFAULT_INDEFINITE):
        self.num = num
        self.degres = degres
        self.indefinite = indefinite

    def __str__(self):
        return f"{self.num} * {self.indefinite}^{self.degres}"
