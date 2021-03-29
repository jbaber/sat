#!/usr/bin/env python3

from itertools import combinations

# Take the 3x3 coords to individual variables
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
def var_from_x_y(x, y):
    try:
        return var_from_x_y.already_given[(x, y)]
    except AttributeError:
        var_from_x_y.already_given = {(x, y): 1}
        return 1
    except KeyError:
        new_var = len(var_from_x_y.already_given) + 1
        var_from_x_y.already_given[(x, y)] = new_var
        return new_var

f = var_from_x_y


def col_coords(col_num):
    for row_num in range(0, 4):
        yield f(col_num, row_num)


def row_coords(row_num):
    for col_num in range(0, 4):
        yield f(col_num, row_num)


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


def main():
    print(cnf_output(exactly_n_true(1, list(row_coords(0)))))
    print(cnf_output(exactly_n_true(1, list(row_coords(1)))))
    print(cnf_output(exactly_n_true(1, list(row_coords(2)))))
    print(cnf_output(exactly_n_true(1, list(row_coords(3)))))
    print(cnf_output(exactly_n_true(1, list(col_coords(0)))))
    print(cnf_output(exactly_n_true(1, list(col_coords(1)))))
    print(cnf_output(exactly_n_true(1, list(col_coords(2)))))
    print(cnf_output(exactly_n_true(1, list(col_coords(3)))))


if __name__ == "__main__":
    main()
