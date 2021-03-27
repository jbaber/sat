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
    yield set(variables)
    for pair in combinations(variables, 2):
        yield set([-x for x in pair])


def cnf_output(clauses):
    to_return = []
    for clause in clauses:
        to_return.append(" ".join(str(x) for x in clause) + " 0")
    return "\n".join(to_return)


def main():
    print(cnf_output(exactly_n_true(row_coords(0), 2)))


if __name__ == "__main__":
    main()
