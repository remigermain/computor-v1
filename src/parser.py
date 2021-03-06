from . import eq, utils, error
import re


class Parser:

    _valid = None

    def __init__(self, line, indefinite=utils.DEFAULT_INDEFINITE):
        self._inde = indefinite
        self._init_regex()
        self.line = self.re_space.sub(" ", line).strip()
        self.errors = error.Error(self.line)

    def _init_regex(self):
        REG_DIGIT = r'\s*-?\s*\d+(?:\.\d+)?\s*'
        REG_FLOAT = r'\s*-?\s*\d+\.\d+\s*'
        LETTER = "{ind1}{ind2}".format(
            ind1=self._inde.upper(), ind2=self._inde.lower())
        REG_LETTER = r'\s*[' + LETTER + r']\s*'
        REG_POWER = REG_LETTER + r"(?:\s*\^\s*" + REG_DIGIT + f"\s*)?"

        REG_ALL = r'([=+]|(?<=[^-+−]\s)-|(?<=[^-+−])-|' + REG_POWER + \
            r'|' + REG_DIGIT + r'|\s+)'

        self.re_split = re.compile(REG_ALL.format(
            ind1=self._inde.upper(), ind2=self._inde.lower()))

        self.re_is_digit = re.compile(r'^' + REG_DIGIT + r'$')

        self.re_is_indefinite = re.compile(REG_LETTER)

        self.re_is_operande = re.compile(r'^\s*[-+−]\s*$')
        self.re_is_equal = re.compile(r"^=$")

        self.re_is_float = re.compile(r'^' + REG_FLOAT + r'$')

        self.re_is_power = re.compile(
            r'^(' + REG_DIGIT + r'(' + REG_POWER + r')?|' + REG_POWER + r')$')

        self.re_space = re.compile(r'\s+')

    @property
    def have_error(self):
        return len(self.errors) != 0

    def get_errors(self):
        return self.errors

    def is_digit(self, value):
        return True if self.re_is_digit.match(value) else False

    def is_float(self, value):
        return True if self.re_is_float.match(value) else False

    def is_indefinite(self, value):
        return True if self.re_is_indefinite.match(value) else False

    def is_operator(self, value):
        return True if self.re_is_operande.match(value) else False

    def is_power(self, value):
        return True if self.re_is_power.match(value) else False

    def is_equal(self, value):
        return True if self.re_is_equal.match(value) else False

    def is_mult(self, value):
        return value in ['*', '∗']

    def split(self, line):
        return self.re_split.split(line)

    def _parse(self, line):
        self.errors.reset()

        if not line or line.isspace():
            self.errors.add_error(self.errors.ERR_EMPTY, 0)
            return False

        self._first_data, self._second_data = [], []  # data before and after equal
        data = self._first_data

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
                    self.errors.add_error(
                        self.errors.ERR_NEED_OPERA, length, val)

                # keep last digit, is will be set in operand or power
                l_digit = round(float(val.replace(' ', '')), 6)
                num, ope = True, False

            elif self.is_power(val):
                # split power , if power have not exposant , default is 1
                _split = val.split("^")
                degres = 1
                if len(data) != 0 and data:
                    self.errors.add_error(
                        self.errors.ERR_NEED_OPERA, length, val)
                if len(_split) != 2:
                    pass
                elif self.is_float(_split[1]):
                    self.errors.add_error(
                        self.errors.ERR_POWER_FLOAT, length, val)
                elif int(_split[1]) < 0:
                    self.errors.add_error(
                        self.errors.ERR_POWER_NEG, length, val)
                else:
                    degres = int(_split[1])
                # if power has not number , default is 1
                if l_digit is None:
                    l_digit = 1

                data.append(eq.Power(l_digit, degres, indefinite=self._inde))

                l_digit = None
                num, ope = True, False

            elif self.is_operator(val):
                if not num or ope:
                    self.errors.add_error(
                        self.errors.ERR_NEED_NUMBER_BF_OPERA, length, val)

                # if number is alone (not power set), the default power is 0
                if l_digit is not None:
                    data.append(eq.Power(l_digit, 0, indefinite=self._inde))

                data.append(eq.Operator(val.strip()))
                num, ope = False, True

            elif self.is_equal(val):
                # append last digit with default power
                if l_digit is not None:
                    data.append(eq.Power(l_digit, 0, indefinite=self._inde))
                    l_digit = None

                # assign error
                if ope:
                    self.errors.add_error(
                        self.errors.ERR_NEED_NUMBER_AF_OPERA, length, val)
                elif equal:
                    self.errors.add_error(self.errors.ERR_UNK, length, val)
                elif not len(data):
                    self.errors.add_error(
                        self.errors.ERR_NOTHING_BF_EQUAL, length, val)

                data = self._second_data
                equal, num, ope = True, False, False

            elif self.is_mult(val):
                if not num or ope:
                    self.errors.add_error(
                        self.errors.ERR_NEED_NUMBER_BF_OPERA, length, val)
                ope = True

            else:
                # unknow type in line
                self.errors.add_error(self.errors.ERR_UNK, length, val)

            length += len(val)

        if l_digit is not None:
            data.append(eq.Power(l_digit, 0, indefinite=self._inde))

        if not self.have_error:
            if not equal:
                self.errors.add_error(self.errors.ERR_MISSING_EQ)
            if ope:
                self.errors.add_error(self.errors.ERR_ENDING_OPE)
            if not num:
                self.errors.add_error(self.errors.ERR_MATH_WRONG)
            if not len(self._second_data):
                self.errors.add_error(self.errors.ERR_NOTHING_AF_EQUAL)

        return not self.have_error

    def is_valid(self):
        if self._valid is None:
            self._valid = self._parse(self.line)
        return self._valid

    @property
    def validated_data(self):
        if self._valid is None:
            raise ValueError(
                "you c'ant access validated data before running is_valid()")
        if self._valid is False:
            raise ValueError("you c'ant access validated data is not valid")
        
        print(self._first_data, self._second_data)
        return self._first_data, self._second_data
