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


def find_intermediates(line: str) -> Bean:
    literals = get_literals_N(line)
    row_index = get_row_index_N(line)
    subeq = get_subeq_N(line)
    return Bean(row_index, line, subeq, literals)


def refind_intermediates(b: Bean) -> Bean:
    literals = get_literals_N(b.subeq)
    b.literals = literals
    return b


if __name__ == '__main__':
    print("*** Main app started ***\n")

    with open('input.txt', 'r', encoding='utf8') as read_file:
        eq = read_file.readline().strip()

        print('Equation literals:')
        eq_literals = find_literals(eq)
        for literal in eq_literals:
            print(literal)

        subsituends = {}  # type: Dict[str, Bean]
        lines = read_file.readlines()
        for line in lines:
            if line is not '' and line is not '\n':
                b = find_intermediates(line.strip())
                subsituends[b.index] = b

        cond = len(subsituends)
        while cond > 0:
            cond = len(subsituends)
            for k, v in subsituends.items():
                if v.literals is not None:
                    for l in v.literals:
                        # print(k + ' ' + l)
                        new = '(' + subsituends[l].subeq + ')'
                        v.subeq = v.subeq.replace(l, new)
                    v = refind_intermediates(v)
                else:
                    cond -= 1

        for eq_l in eq_literals:
            new = '(' + subsituends[eq_l].subeq + ')'
            eq = eq.replace(eq_l, new)

        print('\nFinal equation:')
        # print(eq)

        with open('output.txt', 'w', encoding='utf8') as write_file:
            write_file.write(eq)
            write_file.close()

    print("*** Main app ended ***\n")
