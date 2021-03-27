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
    for variable in variables:
        yield set([-x for x in set(variables).difference([variable])]).union([variable])


def cnf_output(clauses):
    to_return = []
    for clause in clauses:
        to_return.append(" ".join(str(x) for x in clause) + " 0")
    return "\n".join(to_return)


def main():
    print(cnf_output(exactly_n_true(row_coords(0), 2)))


if __name__ == "__main__":
    main()


############
# Unit tests
############

def test_var_from_x_y():

    # Random order to test memoization
    assert var_from_x_y(0, 3) == 1
    assert var_from_x_y(3, 3) == 2
    assert var_from_x_y(0, 0) == 3
    assert var_from_x_y(2, 2) == 4
    assert var_from_x_y(2, 3) == 5
    assert var_from_x_y(3, 1) == 6
    assert var_from_x_y(1, 3) == 7
    assert var_from_x_y(3, 0) == 8
    assert var_from_x_y(2, 0) == 9
    assert var_from_x_y(1, 2) == 10
    assert var_from_x_y(3, 2) == 11
    assert var_from_x_y(0, 2) == 12
    assert var_from_x_y(0, 1) == 13
    assert var_from_x_y(2, 1) == 14
    assert var_from_x_y(1, 0) == 15
    assert var_from_x_y(1, 1) == 16

    assert var_from_x_y(0, 0) == 3
    assert var_from_x_y(0, 1) == 13
    assert var_from_x_y(0, 2) == 12
    assert var_from_x_y(0, 3) == 1
    assert var_from_x_y(1, 0) == 15
    assert var_from_x_y(1, 1) == 16
    assert var_from_x_y(1, 2) == 10
    assert var_from_x_y(1, 3) == 7
    assert var_from_x_y(2, 0) == 9
    assert var_from_x_y(2, 1) == 14
    assert var_from_x_y(2, 2) == 4
    assert var_from_x_y(2, 3) == 5
    assert var_from_x_y(3, 0) == 8
    assert var_from_x_y(3, 1) == 6
    assert var_from_x_y(3, 2) == 11
    assert var_from_x_y(3, 3) == 2


def test_col_coords():
    assert tuple(col_coords(0)) == (1, 2, 3, 4)
    assert tuple(col_coords(1)) == (5, 6, 7, 8)
    assert tuple(col_coords(2)) == (9, 10, 11, 12)
    assert tuple(col_coords(3)) == (13, 14, 15, 16)

def test_row_coords():
    assert tuple(row_coords(0)) == (1, 5, 9, 13)
    assert tuple(row_coords(1)) == (2, 6, 10, 14)
    assert tuple(row_coords(2)) == (3, 7, 11, 15)
    assert tuple(row_coords(3)) == (4, 8, 12, 16)

def test_exactly_1_true():
    assert list(exactly_1_true((1, 2,))) == [
        set([1, 2,]),
        set([-1, -2,]),
    ]
    assert list(exactly_1_true((1, 2, 3,))) == [
        set([1, 2, 3,]),
        set([-1, -2,]),
        set([-2, -3,]),
        set([-1, -3,]),
    ]
    assert list(exactly_1_true((1, 2, 3, 4,))) == [
        set([1, 2, 3, 4,]),
        set([-1, -2,]),
        set([-1, -3,]),
        set([-1, -4,]),
        set([-2, -3,]),
        set([-2, -4,]),
        set([-3, -4,]),
    ]

def test_cnf_output():
    assert cnf_output(((1, -2, 3), (4, 5, -6))) == """1 -2 3 0\n4 5 -6 0"""
