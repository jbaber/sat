import pytest
import generate_4_rooks as g

def test_var_from_x_y():

    # Random order to test memoization
    assert g.var_from_x_y(0, 3) == 1
    assert g.var_from_x_y(3, 3) == 2
    assert g.var_from_x_y(0, 0) == 3
    assert g.var_from_x_y(2, 2) == 4
    assert g.var_from_x_y(2, 3) == 5
    assert g.var_from_x_y(3, 1) == 6
    assert g.var_from_x_y(1, 3) == 7
    assert g.var_from_x_y(3, 0) == 8
    assert g.var_from_x_y(2, 0) == 9
    assert g.var_from_x_y(1, 2) == 10
    assert g.var_from_x_y(3, 2) == 11
    assert g.var_from_x_y(0, 2) == 12
    assert g.var_from_x_y(0, 1) == 13
    assert g.var_from_x_y(2, 1) == 14
    assert g.var_from_x_y(1, 0) == 15
    assert g.var_from_x_y(1, 1) == 16

    assert g.var_from_x_y(0, 0) == 3
    assert g.var_from_x_y(0, 1) == 13
    assert g.var_from_x_y(0, 2) == 12
    assert g.var_from_x_y(0, 3) == 1
    assert g.var_from_x_y(1, 0) == 15
    assert g.var_from_x_y(1, 1) == 16
    assert g.var_from_x_y(1, 2) == 10
    assert g.var_from_x_y(1, 3) == 7
    assert g.var_from_x_y(2, 0) == 9
    assert g.var_from_x_y(2, 1) == 14
    assert g.var_from_x_y(2, 2) == 4
    assert g.var_from_x_y(2, 3) == 5
    assert g.var_from_x_y(3, 0) == 8
    assert g.var_from_x_y(3, 1) == 6
    assert g.var_from_x_y(3, 2) == 11
    assert g.var_from_x_y(3, 3) == 2


def test_col_coords():
    assert tuple(g.col_coords(0)) == (g.f(0, 0), g.f(0, 1), g.f(0, 2), g.f(0, 3))
    assert tuple(g.col_coords(1)) == (g.f(1, 0), g.f(1, 1), g.f(1, 2), g.f(1, 3))
    assert tuple(g.col_coords(2)) == (g.f(2, 0), g.f(2, 1), g.f(2, 2), g.f(2, 3))
    assert tuple(g.col_coords(3)) == (g.f(3, 0), g.f(3, 1), g.f(3, 2), g.f(3, 3))

def test_row_coords():
    assert tuple(g.row_coords(0)) == (g.f(0, 0), g.f(1, 0), g.f(2, 0), g.f(3, 0))
    assert tuple(g.row_coords(1)) == (g.f(0, 1), g.f(1, 1), g.f(2, 1), g.f(3, 1))
    assert tuple(g.row_coords(2)) == (g.f(0, 2), g.f(1, 2), g.f(2, 2), g.f(3, 2))
    assert tuple(g.row_coords(3)) == (g.f(0, 3), g.f(1, 3), g.f(2, 3), g.f(3, 3))

def test_exactly_1_true():
    assert list(g.exactly_1_true((1, 2,))) == [
        (1, 2,),
        (-1, -2,),
    ]
    assert list(g.exactly_1_true((1, 2, 3,))) == [
        (1, 2, 3,),
        (-1, -2,),
        (-1, -3,),
        (-2, -3,),
    ]
    assert list(g.exactly_1_true((1, 2, 3, 4,))) == [
        (1, 2, 3, 4,),
        (-1, -2,),
        (-1, -3,),
        (-1, -4,),
        (-2, -3,),
        (-2, -4,),
        (-3, -4,),
    ]


def test_at_most_n_true():
    assert list(g.at_most_n_true(0, (1,))) == [
        (-1,),
    ]
    assert list(g.at_most_n_true(1, (1,))) == [
    ]
    assert list(g.at_most_n_true(0, (1, 2,))) == [
        (-1,),
        (-2,),
    ]
    assert list(g.at_most_n_true(1, (1, 2,))) == [
        (-1, -2),
    ]
    assert list(g.at_most_n_true(2, (1, 2,))) == [
    ]
    assert list(g.at_most_n_true(0, (1, 2, 3,))) == [
        (-1,),
        (-2,),
        (-3,),
    ]
    assert list(g.at_most_n_true(1, (1, 2, 3,))) == [
        (-1, -2,),
        (-1, -3,),
        (-2, -3,),
    ]
    assert list(g.at_most_n_true(2, (1, 2, 3,))) == [
        (-1, -2, -3,),
    ]
    assert list(g.at_most_n_true(3, (1, 2, 3,))) == [
    ]
    assert list(g.at_most_n_true(0, (1, 2, 3, 4,))) == [
        (-1,),
        (-2,),
        (-3,),
        (-4,),
    ]
    assert list(g.at_most_n_true(1, (1, 2, 3, 4,))) == [
        (-1, -2,),
        (-1, -3,),
        (-1, -4,),
        (-2, -3,),
        (-2, -4,),
        (-3, -4,),
    ]
    assert list(g.at_most_n_true(2, (1, 2, 3, 4,))) == [
        (-1, -2, -3,),
        (-1, -2, -4,),
        (-1, -3, -4,),
        (-2, -3, -4,),
    ]
    assert list(g.at_most_n_true(3, (1, 2, 3, 4,))) == [
        (-1, -2, -3, -4),
    ]
    assert list(g.at_most_n_true(4, (1, 2, 3, 4,))) == [
    ]

    with pytest.raises(ValueError):
        print(list(g.at_most_n_true(4, (1, 2, 3))))
    


def test_at_least_n_true():
    assert list(g.at_least_n_true(0, (1,))) == [
    ]
    assert list(g.at_least_n_true(1, (1,))) == [
        (1,),
    ]
    assert list(g.at_least_n_true(0, (1, 2,))) == [
    ]
    assert list(g.at_least_n_true(1, (1, 2,))) == [
        (1, 2,),
    ]
    assert list(g.at_least_n_true(2, (1, 2,))) == [
        (1,),
        (2,),
    ]
    assert list(g.at_least_n_true(0, (1, 2, 3,))) == [
    ]
    assert list(g.at_least_n_true(1, (1, 2, 3,))) == [
        (1, 2, 3,),
    ]
    assert list(g.at_least_n_true(2, (1, 2, 3,))) == [
        (1, 2,),
        (1, 3,),
        (2, 3,),
    ]
    assert list(g.at_least_n_true(3, (1, 2, 3,))) == [
        (1,),
        (2,),
        (3,),
    ]

    assert list(g.at_least_n_true(0, (1, 2, 3, 4,))) == [
    ]
    assert list(g.at_least_n_true(1, (1, 2, 3, 4,))) == [
        (1, 2, 3, 4,),
    ]
    assert list(g.at_least_n_true(2, (1, 2, 3, 4,))) == [
        (1, 2, 3,),
        (1, 2, 4,),
        (1, 3, 4,),
        (2, 3, 4,),
    ]
    assert list(g.at_least_n_true(3, (1, 2, 3, 4,))) == [
        (1, 2,),
        (1, 3,),
        (1, 4,),
        (2, 3,),
        (2, 4,),
        (3, 4,),
    ]
    assert list(g.at_least_n_true(4, (1, 2, 3, 4,))) == [
        (1,),
        (2,),
        (3,),
        (4,),
    ]

    with pytest.raises(ValueError):
        print(list(g.at_least_n_true(4, (1, 2, 3))))



def test_cnf_output():
    assert g.cnf_output(((1, -2, 3), (4, 5, -6))) == """1 -2 3 0\n4 5 -6 0"""
