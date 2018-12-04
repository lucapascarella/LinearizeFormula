import re

from typing import List, Dict

from Bean import Bean


def get_literals_N(msg: str) -> [str]:
    regex = r"\s*(N\d+)\*"

    matches = re.findall(regex, msg)
    if matches:
        return matches
    return None


def get_row_index_N(msg: str) -> str:
    regex = r"^(N\d+)\W*="

    matches = re.findall(regex, msg)
    if matches:
        return matches[0]
    return None


def get_subeq_N(msg: str) -> str:
    regex = r"^N\d+\W*=\s*(.*)"

    matches = re.findall(regex, msg)
    if matches:
        return matches[0]
    return None


def find_literals(line: str) -> [str]:
    literals = get_literals_N(line)
    return literals


def get_literal_bean(line: str) -> Bean:
    literals = get_literals_N(line)
    row_index = get_row_index_N(line)
    subeq = get_subeq_N(line)
    return Bean(row_index, line, subeq, literals)


def update_literal_bean(b: Bean) -> Bean:
    literals = get_literals_N(b.subeq)
    b.literals = literals
    return b


def return_len_unit(len: int) -> str:
    new = len / 1024
    if new < 0:
        return str(len)
    else:
        new2 = new / 1024
        if new2 < 0:
            return str(new + ' k')


if __name__ == '__main__':
    print("*** Main app started ***\n")

    with open('data/input.txt', 'r', encoding='ascii') as read_file:

        # Find literals of the main equation
        # print('Main eq literals:')
        eq = read_file.readline().strip()
        # eq_literals = find_literals(eq)
        # print(', '.join(eq_literals))

        # Index remaining lines by left literal
        substitutions = {}  # type: Dict[str, Bean]
        for line in read_file.readlines():
            line = line.strip()
            if line is not '':
                b = get_literal_bean(line)
                substitutions[b.index] = b

        # Perform last substitution in the main equation
        iteration = 0
        exit_while = False
        while exit_while is False:
            eq_literals = find_literals(eq)
            if eq_literals is None:
                exit_while = True
            else:
                print('Iteration: {}, Found: {} literals'.format(iteration, len(eq_literals)))
                for eq_l in eq_literals:
                    new = '(' + substitutions[eq_l].subeq + ')'
                    eq = eq.replace(eq_l, new)
            iteration += 1

        # Print results
        print('\nFinal equation length: {} bytes'.format(len(eq)))

        # Save equation
        with open('data/output.txt', 'w', encoding='utf8') as write_file:
            write_file.write(eq)
            write_file.close()

    print("*** Main app ended ***\n")
