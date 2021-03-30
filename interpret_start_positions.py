#!/usr/bin/env python3

import sys
import re


ROW_COR = {
    'a': 1,
    'b': 2,
    'c': 3,
    'd': 4,
    'e': 5,
    'f': 6,
    'g': 7,
    'h': 8,
    'i': 9,
    'A': 1,
    'B': 2,
    'C': 3,
    'D': 4,
    'E': 5,
    'F': 6,
    'G': 7,
    'H': 8,
    'I': 9,
}


def get_start_positions(filename):
    to_return = {}
    with open(filename) as f:
        for line in f:
            line = line.strip()
            try:
                row_num = int(line[0])
            except ValueError:
                row_num = ROW_COR[line[0]]
            col_num = int(line[1])
            value   = int(line[2])
            to_return[(row_num, col_num)] = value
    return to_return


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


# def cnf_output(start_positions, correspondence):


def plot_start_positions(start_positions):
    s = {}
    to_return = """+-----+-----+-----+
|{} {} {}|{} {} {}|{} {} {}|
|{} {} {}|{} {} {}|{} {} {}|
|{} {} {}|{} {} {}|{} {} {}|
+-----+-----+-----+
|{} {} {}|{} {} {}|{} {} {}|
|{} {} {}|{} {} {}|{} {} {}|
|{} {} {}|{} {} {}|{} {} {}|
+-----+-----+-----+
|{} {} {}|{} {} {}|{} {} {}|
|{} {} {}|{} {} {}|{} {} {}|
|{} {} {}|{} {} {}|{} {} {}|
+-----+-----+-----+"""
    for i in range(0, 10):
        for j in range(0, 10):
            s[(i, j)] = ' '

    for coords, value in start_positions.items():
        s[coords] = value

    return to_return.format(
        s[(1, 1)], s[(1, 2)], s[(1, 3)], s[(1, 4)], s[(1, 5)], s[(1, 6)], s[(1, 7)], s[(1, 8)], s[(1, 9)],
        s[(2, 1)], s[(2, 2)], s[(2, 3)], s[(2, 4)], s[(2, 5)], s[(2, 6)], s[(2, 7)], s[(2, 8)], s[(2, 9)],
        s[(3, 1)], s[(3, 2)], s[(3, 3)], s[(3, 4)], s[(3, 5)], s[(3, 6)], s[(3, 7)], s[(3, 8)], s[(3, 9)],
        s[(4, 1)], s[(4, 2)], s[(4, 3)], s[(4, 4)], s[(4, 5)], s[(4, 6)], s[(4, 7)], s[(4, 8)], s[(4, 9)],
        s[(5, 1)], s[(5, 2)], s[(5, 3)], s[(5, 4)], s[(5, 5)], s[(5, 6)], s[(5, 7)], s[(5, 8)], s[(5, 9)],
        s[(6, 1)], s[(6, 2)], s[(6, 3)], s[(6, 4)], s[(6, 5)], s[(6, 6)], s[(6, 7)], s[(6, 8)], s[(6, 9)],
        s[(7, 1)], s[(7, 2)], s[(7, 3)], s[(7, 4)], s[(7, 5)], s[(7, 6)], s[(7, 7)], s[(7, 8)], s[(7, 9)],
        s[(8, 1)], s[(8, 2)], s[(8, 3)], s[(8, 4)], s[(8, 5)], s[(8, 6)], s[(8, 7)], s[(8, 8)], s[(8, 9)],
        s[(9, 1)], s[(9, 2)], s[(9, 3)], s[(9, 4)], s[(9, 5)], s[(9, 6)], s[(9, 7)], s[(9, 8)], s[(9, 9)],
    )


def main():
    if len(sys.argv) != 3:
        print("Usage: {} <cnf-file.cnf> <starting_positions-file>".format(sys.argv[0]))
        print("positions look like \"a12\" to mean row a, col 1 has a 2 in it.")
        exit(1)

    correspondence = get_correspondence(sys.argv[1])

    print(plot_start_positions(get_start_positions(sys.argv[2])))
    print("\n-------\n")
    # print(cnf_output(start_positions, correspondence))


if __name__ == "__main__":
    main()
