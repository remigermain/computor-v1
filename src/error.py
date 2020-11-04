
class Error:

    message = {
        "ERR_EMPTY": 'String is empty.',
        "ERR_NEED_OPERA": "you need a operator between number.",
        "ERR_MAX_DEGRES": "your degres is upper than {degres}, c\'ant be resolve.",
        "ERR_NEED_NUMBER_BF_OPERA": "you need a number befor operator.",
        "ERR_NEED_NUMBER_AF_OPERA": "you need a number after operator.",
        "ERR_UNK": "unknow type.",
        "ERR_NOTHING_BF_EQUAL": "he have nothing before equal ...",
        "ERR_MISSING_EQ": "missing equal.",
        "ERR_ENDING_OPE": "a calcul c\'ant ending by operator.",
        "ERR_MATH_WRONG": "Your math is wrong ..."
    }

    def __init__(self):
        self._keys = list(self.message.keys())
        for idx, attr in enumerate(self._keys):
            setattr(self, attr, idx)

    def get_message(self, item, **kwargs):
        return self.message[self._keys[item]].format(**kwargs)
