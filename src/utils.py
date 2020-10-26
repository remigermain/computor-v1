
MAX_DEGRES = 2
DEFAULT_INDEFINITE = "x"

RED = ""
WHITE = ""


def error_line(line, errors):
    print('\nError in line:')
    for error in errors:
        print(error[0])
        print('\t' + line)
        space_min = " " * error[0][0] if error[0][0] else ""
        space_max = "^" * error[0][1] if error[0][1] else "^"
        print('\t' + space_min + RED + space_max + WHITE)
        print('\t' + space_min + error[1])


def print_results(results):
    for r in results:
        if r['have_error']:
            error_line(r['parser'].line, r['parser']._errors)
        else:
            print("NICE")


def lst_poly_str(lst):
    return ' '.join(map(str, lst))
