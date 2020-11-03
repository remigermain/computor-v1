from . import poly, utils
import re
import enum

re_space = re.compile(r"\s+")

Error = enum.Enum('Error', (
    "ERR_EMPTY",
    "ERR_NEED_OPERA",
    "ERR_MAX_DEGRES",
    "ERR_NEED_NUMBER_BF_OPERA",
    "ERR_NEED_NUMBER_AF_OPERA",
    "ERR_UNK",
    "ERR_NOTHING_BF_EQUAL",
    "ERR_MISSING_EQ",
    "ERR_ENDING_OPE",
    "ERR_MATH_WRONG"
)
)


class Parser:

    _valid = None
    _errors = []

    def __init__(self, line, indefinite=utils.DEFAULT_INDEFINITE):
        self._inde = indefinite
        self._init_regex()
        self.line = self.re_space.sub(" ", line)

    def _init_regex(self):
        REG_DIGIT = r'\s*-?\s*\d+(?:\.\d+)?\s*'
        LETTER = "{ind1}{ind2}".format(
            ind1=self._inde.upper(), ind2=self._inde.lower())
        REG_LETTER = r'\s*[' + LETTER + r']\s*'
        REG_POWER = REG_LETTER + r"(?:\s*\^\s*\d+\s*)?"

        REG_ALL = r'([=+]|(?<=[^-]\s)-|' + REG_POWER + \
            r'|' + REG_DIGIT + r'|\s+)'

        self.re_split = re.compile(REG_ALL.format(
            ind1=self._inde.upper(), ind2=self._inde.lower()))

        self.re_is_digit = re.compile(r'^' + REG_DIGIT + r'$')

        self.re_is_indefinite = re.compile(REG_LETTER)

        self.re_is_operande = re.compile(r'^\s*[-+]\s*$')
        self.re_is_equal = re.compile(r"^=$")

        self.re_is_power = re.compile(
            r'^(' + REG_DIGIT + r'(' + REG_POWER + r')?|' + REG_POWER + r')$')

        self.re_space = re.compile(r'\s+')

    @property
    def have_error(self):
        return len(self._errors) != 0

    def is_digit(self, value):
        return True if self.re_is_digit.match(value) else False

    def is_indefinite(self, value):
        return True if self.re_is_indefinite.match(value) else False

    def is_operande(self, value):
        return True if self.re_is_operande.match(value) else False

    def is_power(self, value):
        return True if self.re_is_power.match(value) else False

    def is_equal(self, value):
        return True if self.re_is_equal.match(value) else False

    def is_mult(self, value):
        return value == '*'

    def split(self, line):
        return self.re_split.split(line)

    def add_error(self, error_type, start, padding, message):
        op = {
            "start": start,
            "padding": padding,
            "message": message
        }
        if error_type not in self._errors:
            self._errors[error_type] = [op]
        else:
            self._errors[error_type].append(op)

    def _parse(self, line):
        self._errors = {}
        if not line or line.isspace():
            self.add_error(Error.ERR_EMPTY, 0, 0, 'String is empty')
            return False

        self._befor_data, self._after_data = [], []  # data before and after equal
        data = self._befor_data

        num, ope, equal, mult = [False] * 4
        _last_digit, _last_val = [None] * 2
        length = 0

        for val in self.split(line):
            _last_val = val

            # if is space of empty string , pass
            if not val:
                continue
            if val.isspace():
                pass

            # if is digit , add in last_digit for waiting the next value
            elif self.is_digit(val):
                if num:
                    self.add_error(Error.ERR_NEED_OPERA,
                                   length, len(val.strip()),
                                   'you need a operator between number.'
                                   )

                _last_digit = val.replace(' ', '')
                num, ope = True, False

            elif self.is_power(val):
                _split = val.split("^")
                degres = 1 if len(_split) != 2 else int(_split[1])
                if _last_digit is None:
                    _last_digit = 1
                data.append(poly.PolyPower(val, float(_last_digit),
                                           degres, indefinite=self._inde))
                if degres > utils.MAX_DEGRES:
                    self.add_error(Error.ERR_MAX_DEGRES,
                                   length, len(val.strip()),
                                   f'your degres is upper than {utils.MAX_DEGRES}, c\'ant be resolve.'
                                   )
                _last_digit = None
                num, ope = True, False

            elif self.is_operande(val):
                if not num or ope:
                    self.add_error(Error.ERR_NEED_NUMBER_BF_OPERA, length, len(
                        val.strip()), 'you need a number befor operator.')
                if _last_digit is not None:
                    data.append(poly.PolyPower(
                        val, float(_last_digit), 1, indefinite=self._inde))
                data.append(poly.PolyOperande(val.strip()))
                num, ope = False, True

            elif self.is_equal(val):
                if _last_digit is not None:
                    data.append(poly.PolyPower(
                        val, float(_last_digit), 1, indefinite=self._inde))
                _last_digit = None

                if ope:
                    self.add_error(Error.ERR_NEED_NUMBER_AF_OPERA, length, len(
                        val.strip()), 'you need a number after operator.')
                elif equal:
                    self.add_error(Error.ERR_UNK, length, len(
                        val.strip()), 'unknow type.')
                elif not len(data):
                    self.add_error(Error.ERR_NOTHING_BF_EQUAL, length, len(
                        val.strip()), 'he have nothing before equal ...')
                data = self._after_data
                equal, num, ope = True, False, False

            elif self.is_mult(val):
                if not num or ope:
                    self.add_error(Error.ERR_NEED_NUMBER_BF_OPERA, length, len(
                        val.strip()), 'you need a number befor operator.')
                ope = True

            else:
                print(val)
                self.add_error(Error.ERR_UNK, length, len(
                    val.strip()), 'unknow type.')
            length += len(val)

        if not self.have_error:
            if not equal:
                self.add_error(Error.ERR_MISSING_EQ, 0,
                               length, 'missing equal.')
            if ope:
                self.add_error(Error.ERR_ENDING_OPE, 0, length,
                               'a calcul c\'ant ending by operator.')
            if not num:
                self.add_error(Error.ERR_MATH_WRONG, 0, length,
                               'Your math is wrong ...')

        if _last_digit is not None:
            data.append(poly.PolyPower(_last_val, int(
                _last_digit), 1, indefinite=self._inde))

        return not self.have_error

    def is_valid(self):
        self._valid = self._parse(self.line)
        return self._valid

    @property
    def validated_data(self):
        if self._valid is None:
            raise ValueError(
                "you c'ant access validated data before running is_valid()")
        if self._valid is False:
            raise ValueError("you c'ant access validated with valid is False")

        return self._befor_data, self._after_data
