from .utils import Color, MAX_DEGRES


class Error:

    message = {
        "ERR_EMPTY": 'String is empty.',
        "ERR_NEED_OPERA": "you need a operator between number.",
        "ERR_MAX_DEGRES": f"your degres is upper than {MAX_DEGRES}, c\'ant be resolve.",
        "ERR_NEED_NUMBER_BF_OPERA": "you need a number befor operator.",
        "ERR_NEED_NUMBER_AF_OPERA": "you need a number after operator.",
        "ERR_UNK": "unknow type.",
        "ERR_NOTHING_BF_EQUAL": "he have nothing valid before equal ...",
        "ERR_NOTHING_AF_EQUAL": "he have nothing valid after equal ...",
        "ERR_MISSING_EQ": "missing equal.",
        "ERR_ENDING_OPE": "a calcul c\'ant ending by operator.",
        "ERR_MATH_WRONG": "Your math is wrong ..."
    }

    _errors = {}

    def __init__(self, line):
        self.line = line
        self._keys = list(self.message.keys())
        for idx, attr in enumerate(self._keys):
            setattr(self, attr, idx)

    def __len__(self):
        return len(self._errors.keys())

    def reset(self):
        self._errors = {}

    def get_message(self, item, **kwargs):
        return self.message[self._keys[item]]

    def add_error(self, idx, start=0, value=""):
        l_strip = value.lstrip()
        op = {
            "start": start + (len(value) - len(l_strip)),
            "padding": len(l_strip.strip()),
            "message": self.get_message(idx)
        }
        if op['start'] == 0 and op['padding'] == 0:
            idx = "start"
        if idx not in self._errors:
            self._errors[idx] = [op]
        else:
            self._errors[idx].append(op)

    def print_error(self):
        print(f'{Color.RED}Error{Color.WHITE}:')
        new_line = False
        for _, error in self._errors.items():
            if new_line:
                print("")
            if self.line:
                print('\t' + self.line)
            last = 0
            space = ""
            messages = []
            for err in error:
                space += " " * (err['start'] - last)
                last = err['start'] + err['padding']
                padd = "^" * err['padding']
                if len(padd):
                    space += Color.RED + padd + Color.WHITE
                if err['message'] not in messages:
                    messages.append(err['message'])
            mess = '\n\t'.join(messages)
            if space:
                print(f"\t{space}")
            print(f"\t{mess}")
            new_line = True
