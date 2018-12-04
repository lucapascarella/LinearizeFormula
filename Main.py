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


if __name__ == '__main__':
    print("*** Main app started ***\n")

    with open('data/input.txt', 'r', encoding='utf8') as read_file:

        # Find literals of the main equation
        print('Main eq literals:')
        eq = read_file.readline().strip()
        eq_literals = find_literals(eq)
        ll = ', '.join(eq_literals)
        print(ll)

        # Index remaining lines by left literal
        substituends = {}  # type: Dict[str, Bean]
        for line in read_file.readlines():
            line = line.strip()
            if line is not '':
                b = get_literal_bean(line)
                substituends[b.index] = b

        # This is a recursive problem, but we can address in a inefficient linear way
        index = 0
        cond = len(substituends)
        while cond > 0:
            cond = len(substituends)
            for k, v in substituends.items():
                if v.literals is not None:
                    for l in v.literals:
                        # print(k + ' ' + l)
                        new = '(' + substituends[l].subeq + ')'
                        v.subeq = v.subeq.replace(l, new)
                    v = update_literal_bean(v)
                else:
                    cond -= 1
            index +=1

        print('Eqs cleaned in: {} steps'.format(index))

        # Perform last substitution in the main equation
        for eq_l in eq_literals:
            new = '(' + substituends[eq_l].subeq + ')'
            eq = eq.replace(eq_l, new)

        print('\nFinal equation:')
        # print(eq)

        with open('data/output.txt', 'w', encoding='utf8') as write_file:
            write_file.write(eq)
            write_file.close()

    print("*** Main app ended ***\n")
