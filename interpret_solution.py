#!/usr/bin/env python3

import sys
import re


def get_correspondence(filename):
    to_return = {}
    regex = re.compile(r'^c ([0-9]+): \(([0-9]+), ([0-9]+)\) is a ([0-9]+)')
    with open(filename) as f:
        for line in f:
            maybe = regex.match(line)
            if maybe:
                to_return[int(maybe[1])] = {'row_num': int(maybe[2]),
                        'col_num': int(maybe[3]), 'value': int(maybe[4])}
    return to_return


def get_solution(filename):
    regex = re.compile(r'^v (-?[0-9]+ )+ ?0')
    with open(filename) as f:
        for line in f:
            maybe = regex.match(line.strip())
            if maybe:
                return [
                    int(x)
                    for x in line.split(' ')[1:-1]
                    if not x.startswith('-')
                ]

def plot_solution(solution, correspondence):
    to_return = ""
    for entry in solution:
        to_return += str(correspondence[entry]) + "\n"
    return to_return


def main():
    if len(sys.argv) != 3:
        print("Usage: {} <cnf-file.cnf> <solution-file>".format(sys.argv[0]))
        exit(1)

    correspondence = get_correspondence(sys.argv[1])

    solution = get_solution(sys.argv[2])
    print(plot_solution(solution, correspondence))


if __name__ == "__main__":
    main()
