#!/usr/bin/env python3

from itertools import combinations

# Take sudoku coords and value to individual variables
#
# Done by just handing out memoized sequential
# naturals instead of being witty because this
# generalizes
#
# Don't output 0 since that can't be negated
# in the cnf input
# 
# Lots of interesting choices for static variable at
# https://stackoverflow.com/questions/279561/what-is-the-python-equivalent-of-static-variables-inside-a-function
# I choose raising an exception
#
# Top-left corner is 1, 1, top-right is 1, 9, bottom-left is 9, 1, bottom-right is 9, 9
# Values run from 1 to 9 as expected
def var_from_x_y_z(row_num, col_num, value):
    if row_num not in range(1, 10) or col_num not in range(1, 10) or \
            value not in range(1, 10):
        raise ValueError("All values should be in 1 - 9")
    try:
        return var_from_x_y_z.already_given[(row_num, col_num, value)]
    except AttributeError:
        var_from_x_y_z.already_given = {(row_num, col_num, value): 1}
        print("c {}: ({}, {}) is a {}".format(1,
                row_num, col_num, value))
        return 1
    except KeyError:
        new_var = len(var_from_x_y_z.already_given) + 1
        var_from_x_y_z.already_given[(row_num, col_num, value)] = new_var
        print("c {}: ({}, {}) is a {}".format(new_var,
                row_num, col_num, value))
        return new_var
f = var_from_x_y_z


def x_y_z_from_var(var):
    if var < 1:
        raise ValueError("All values should be bigger than 1")
    try:
        keys = [
            key
            for key, value in var_from_x_y_z.already_given.items()
            if value == var
        ]
        if len(keys) == 0:
            raise RuntimeError("No value corresponding to {}".format(var))
        if len(keys) > 1:
            raise RuntimeError("Something corrupted, more than one value"
                    "corresponding to {}".format(var))
        return keys[0]
    except AttributeError:
        raise RuntimeError("No variables have been handed out yet!")


def exactly_1_true(variables):
    for tup in at_least_n_true(1, variables):
        yield tup
    for tup in at_most_n_true(1, variables):
        yield tup


def exactly_n_true(n, variables):
    for tup in at_least_n_true(n, variables):
        yield tup
    for tup in at_most_n_true(n, variables):
        yield tup



def at_most_n_true(n, variables):
    if n > len(variables):
        raise ValueError("Can't have {} true when only {} variables given.".format(n, len(variables)))
    for combo in combinations(variables, n + 1):
        yield tuple(-variable for variable in combo)


def at_least_n_true(n, variables):
    difference = len(variables) - n
    if difference < 0:
        raise ValueError("Can't have {} true when only {} variables given.".format(n, len(variables)))
    else:
        for combo in combinations(variables, difference + 1):
            yield combo



def cnf_output(clauses):
    to_return = []
    for clause in clauses:
        to_return.append(" ".join(str(x) for x in clause) + " 0")
    return "\n".join(to_return)


def nonant_coords(description):
    if description in ("nw", 1):
        return ((1, 1), (1, 2), (1, 3),
                (2, 1), (2, 2), (2, 3),
                (3, 1), (3, 2), (3, 3),
        )
    if description in ("n", 2):
        return ((1, 4), (1, 5), (1, 6),
                (2, 4), (2, 5), (2, 6),
                (3, 4), (3, 5), (3, 6),
        )
    if description in ("ne", 3):
        return ((1, 7), (1, 8), (1, 9),
                (2, 7), (2, 8), (2, 9),
                (3, 7), (3, 8), (3, 9),
        )
    if description in ("w", 4):
        return ((4, 1), (4, 2), (4, 3),
                (5, 1), (5, 2), (5, 3),
                (6, 1), (6, 2), (6, 3),
        )
    if description in ("c", 5):
        return ((4, 4), (4, 5), (4, 6),
                (5, 4), (5, 5), (5, 6),
                (6, 4), (6, 5), (6, 6),
        )
    if description in ("e", 6):
        return ((4, 7), (4, 8), (4, 9),
                (5, 7), (5, 8), (5, 9),
                (6, 7), (6, 8), (6, 9),
        )
    if description in ("sw", 7):
        return ((7, 1), (7, 2), (7, 3),
                (8, 1), (8, 2), (8, 3),
                (9, 1), (9, 2), (9, 3),
        )
    if description in ("s", 8):
        return ((7, 4), (7, 5), (7, 6),
                (8, 4), (8, 5), (8, 6),
                (9, 4), (9, 5), (9, 6),
        )
    if description in ("se", 9):
        return ((7, 7), (7, 8), (7, 9),
                (8, 7), (8, 8), (8, 9),
                (9, 7), (9, 8), (9, 9),
        )

    raise ValueError("Only nw,n,ne,w,c,e,sw,s,se allowed")



def main():

    # Only one value for entry i, j
    for i in range(1, 10):
        for j in range(1, 10):
            print(cnf_output(exactly_1_true([f(i, j, k) for k in range(1, 10)])))

    # Only one in k-th row is a j
    for k in range(1, 10):
        for j in range(1, 10):
            print(cnf_output(exactly_1_true([f(k, i, j) for i in range(1, 10)])))

    # Only one in k-th column is a j
    for k in range(1, 10):
        for j in range(1, 10):
            print(cnf_output(exactly_1_true([f(i, k, j) for i in range(1, 10)])))

    # Only one in k-th nonant is a j
    for k in range(1, 10):
        for j in range(1, 10):
            print(cnf_output(
                exactly_1_true([
                    f(coord[0], coord[1], j)
                    for coord in nonant_coords(k)
                ])
            ))


if __name__ == "__main__":
    main()
