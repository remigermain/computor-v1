from . import eq, utils, error
import re

re_space = re.compile(r"\s+")
Error = error.Error()


class Parser:

    _valid = None
    _errors = []

    def __init__(self, line, indefinite=utils.DEFAULT_INDEFINITE):
        self._inde = indefinite
        self._init_regex()
        self.line = self.re_space.sub(" ", line)

    def _init_regex(self):
        # TODO fix negative number
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

        self.re_is_operande = re.compile(r'^\s*[-+−]\s*$')
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

    def add_error(self, error_type, start=-1, _str="", **kwargs):
        l_strip = _str.lstrip()
        op = {
            "start": start + (len(_str) - len(l_strip)),
            "padding": len(l_strip),
            "message": Error.get_message(error_type, **kwargs)
        }
        if error_type not in self._errors:
            self._errors[error_type] = [op]
        else:
            self._errors[error_type].append(op)

    def _parse(self, line):
        self._errors = {}

        if not line or line.isspace():
            self.add_error(Error.ERR_EMPTY, 0, 0)
            return False

        self._befor_data, self._after_data = [], []  # data before and after equal
        data = self._befor_data

        # boolean to know order in parsing
        num, ope, equal, mult = [False] * 4
        l_digit = None

        # lenght line for error
        length = 0
        for val in self.split(line):
            # if is space of empty string , pass
            if val.isspace() or not len(val):
                pass

            # if is digit , add in last_digit for waiting the next value
            elif self.is_digit(val):
                if num:
                    self.add_error(Error.ERR_NEED_OPERA, length, val)

                # keep last digit, is will be set in operand or power
                l_digit = float(val.replace(' ', ''))
                num, ope = True, False

            elif self.is_power(val):
                # split power , if power have not exposant , default is 1
                _split = val.split("^")
                degres = 1 if len(_split) != 2 else int(_split[1])

                # if power has not number , default is 1
                if l_digit is None:
                    l_digit = 1

                # degres c'ant be upper than max degres
                if degres > utils.MAX_DEGRES:
                    self.add_error(Error.ERR_MAX_DEGRES, length,
                                   val, degres=utils.MAX_DEGRES)
                data.append(eq.Power(l_digit, degres, indefinite=self._inde))

                l_digit = None
                num, ope = True, False

            elif self.is_operande(val):
                if not num or ope:
                    self.add_error(Error.ERR_NEED_NUMBER_BF_OPERA, length, val)

                # if number is alone (not power set), the default power is 0
                if l_digit is not None:
                    data.append(eq.Power(l_digit, 0, indefinite=self._inde))

                data.append(eq.Operande(val.strip()))
                num, ope = False, True

            elif self.is_equal(val):
                # append last digit with default power
                if l_digit is not None:
                    data.append(eq.Power(l_digit, 0, indefinite=self._inde))
                    l_digit = None

                # assign error
                if ope:
                    self.add_error(Error.ERR_NEED_NUMBER_AF_OPERA, length, val)
                elif equal:
                    self.add_error(Error.ERR_UNK, length, val)
                elif not len(data):
                    self.add_error(Error.ERR_NOTHING_BF_EQUAL, length, val)

                data = self._after_data
                equal, num, ope = True, False, False

            elif self.is_mult(val):
                if not num or ope:
                    self.add_error(Error.ERR_NEED_NUMBER_BF_OPERA, length, val)
                ope = True

            else:
                # unknow type in line
                self.add_error(Error.ERR_UNK, length, val)

            length += len(val)

        if not self.have_error:
            if not equal:
                self.add_error(Error.ERR_MISSING_EQ)
            if ope:
                self.add_error(Error.ERR_ENDING_OPE)
            if not num:
                self.add_error(Error.ERR_MATH_WRONG)

        if l_digit is not None:
            data.append(eq.Power(l_digit, 0, indefinite=self._inde))

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
            raise ValueError("you c'ant access validated data is not valid")

        return self._befor_data, self._after_data
