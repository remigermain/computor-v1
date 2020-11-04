
MAX_DEGRES = 2
DEFAULT_INDEFINITE = "x"


class Color:
    PURPLE = '\033[1;35;48m'
    CYAN = '\033[1;36;48m'
    BOLD = '\033[1;37;48m'
    BLUE = '\033[1;34;48m'
    GREEN = '\033[1;32;48m'
    YELLOW = '\033[1;33;48m'
    RED = '\033[1;31;48m'
    BLACK = '\033[1;30;48m'
    UNDERLINE = '\033[4;37;48m'
    END = '\033[1;37;0m'
    WHITE = '\033[1;39;0m'


def error_line(line, errors):
    print(f'{Color.RED}Error{Color.WHITE}:')
    new_line = False
    for key in errors:
        if new_line:
            print("")
        if line:
            print('\t' + line)
        last = 0
        space = ""
        messages = []
        for err in errors[key]:
            space += " " * (err['start'] - last)
            last = err['start'] + err['padding']
            padd = "^" * err['padding']
            if len(padd):
                space += Color.RED + padd + Color.WHITE
            if err['message'] not in messages:
                messages.append(err['message'])
        mess = '\n'.join(messages)
        if space:
            print(f"\t{space}")
        print(f"\t{mess}")
        new_line = True


def print_results(results):
    new_line = False
    for r in results:
        if new_line:
            print("\n")
        if r['have_error']:
            error_line(r['parser'].line, r['parser']._errors)
        else:
            r['resolve'].resolve()
        new_line = True


def lst_poly_str(lst):
    return ' '.join(map(str, lst))
