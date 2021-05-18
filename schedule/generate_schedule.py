#!/usr/bin/env python3

import sys
import json
from itertools import combinations
from itertools import product

# Take schedule coords and value to individual variables
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
def var_from_period_teacher_course(period, teacher, course, config):
    teachers = config["teachers"]
    courses = config["courses"]
    periods = config["periods"]

    if teacher not in teachers:
        raise ValueError(f"{teacher} not in  {teachers}")
    if period not in periods:
        raise ValueError(f"{period} not in {periods}")
    if course not in courses:
        raise ValueError(f"{course} not in {courses}")

    try:
        return var_from_period_teacher_course.already_given[(teacher, period, course)]
    except AttributeError:
        var_from_period_teacher_course.already_given = {(teacher, period, course): 1}
        print("c {}: {} teaches {} period {}".format(1, teacher, course, period))
        return 1
    except KeyError:
        new_var = len(var_from_period_teacher_course.already_given) + 1
        var_from_period_teacher_course.already_given[(teacher, period, course)] = new_var
        print("c {}: {} teaches {} period {}".format(new_var, teacher, course, period))
        return new_var
f = var_from_period_teacher_course


def teacher_period_course_from_var(var):
    if var < 1:
        raise ValueError("All values should be bigger than 1")
    try:
        keys = [
            key
            for key, value in var_from_period_teacher_course.already_given.items()
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


def test_and_of_ors_from_ors_of_ands():
    # 1 v 3^4 v 5^6 = (1v3 ^ 1v4) v (5^6) = ((1v3 ^ 1v4) v 5) ^ ((1v3 ^ 1v4) v 6)
    # = (1v3v5 ^ 1v4v5) ^ (1v3v6 ^ 1v4v6)
    assert set(and_of_ors_from_ors_of_ands(((1,), (3, 4), (5,6)))) == set([(1, 3, 5), (1, 4, 5), (1, 3, 6), (1, 4, 6)])
    # 1^2 v 3^4 v 5^6 = (1 v (3^4 v 5^6)) ^ (2 v (364 v 5^6))
    # = (1v3v5 ^ 1v4v5) ^ (1v3v6 ^ 1v4v6) ^ (2v3v5 ^ 2v4v5) ^ (2v3v6 ^ 2v4v6)
    assert set(and_of_ors_from_ors_of_ands(((1, 2), (3, 4), (5, 6)))) == \
    set(((1, 3, 5), (1, 4, 5), (1, 3, 6), (1, 4, 6), (2, 3, 5), (2, 4, 5), (2, 3, 6),  (2, 4, 6),))

    # Degrades to and_of_ors_from_or_of_ands (copying those tests)
    assert and_of_ors_from_ors_of_ands(((1,), ())) == [(1,)]
    assert and_of_ors_from_ors_of_ands(((1,), (2,))) == [((1, 2))]
    assert and_of_ors_from_ors_of_ands(((1, 2), (3,))) == [(1, 3), (2, 3)]
    assert and_of_ors_from_ors_of_ands(((1,), (2, 3))) == [(1, 2), (1, 3)]
    assert and_of_ors_from_ors_of_ands(((1, 2), (3, 4))) == [(1, 3), (1, 4), (2, 3), (2, 4)]
    assert and_of_ors_from_ors_of_ands(((1,), (2, 3, 4))) == [(1, 2), (1, 3), (1, 4)]



def test_and_of_ors_from_or_of_ands():
    # (1) v () = (1)
    assert and_of_ors_from_or_of_ands((1,), ()) == [(1,)]
    # (1) v (2) = (1 v 2)
    assert and_of_ors_from_or_of_ands((1,), (2,)) == ([(1, 2)])
    # (1 ^ 2) v 3 = (1 v 3) ^ (2 v 3)
    assert and_of_ors_from_or_of_ands((1, 2), (3,)) == [(1, 3), (2, 3)]
    # (1) v (2 ^ 3) = (1 v 2) ^ (1 v 3)
    assert and_of_ors_from_or_of_ands((1,), (2, 3)) == [(1, 2), (1, 3)]
    # (1 ^ 2) v (3 ^ 4) = (1 v (3 ^ 4)) ^ (2 v (3 ^ 4)) = (1v3 ^ 1v4) ^ (2v3 ^ 2v4)
    assert and_of_ors_from_or_of_ands((1, 2), (3, 4)) == [(1, 3), (1, 4), (2, 3), (2, 4)]
    # (1) v (2 ^ 3 ^ 4) = (1v2 ^ 1v3 ^ 1v4)
    assert and_of_ors_from_or_of_ands((1,), (2, 3, 4)) == [(1, 2), (1, 3), (1, 4)]


# Convert (1^2^3^4) v (5^6^7^8) to (.v.v.) ^ (.v.v.) ^ (.v.v.) ^ ...
def and_of_ors_from_or_of_ands(lefty, righty):
    if len(lefty) == 0:
        return [righty]
    if len(righty) == 0:
        return [lefty]

    return list(product(*[lefty, righty]))


# Like and_of_ors_from_or_of_ands, but takes more than two
def and_of_ors_from_ors_of_ands(arr_of_ands):

    # Remove empty arrays since they make the product empty
    arr_of_ands = [
        arr
        for arr in arr_of_ands
        if arr != None and len(arr) > 0
    ]
    return list(product(*arr_of_ands))


def cnf_output(clauses):
    to_return = []
    for clause in clauses:
        to_return.append(" ".join(str(x) for x in clause) + " 0")
    return "\n".join(to_return)


def main():

    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <conf.json>")
        exit(1)

    with open(sys.argv[1]) as g:
        config = json.load(g)

    courses = config["courses"]
    teachers = config["teachers"]
    periods = config["periods"]

    # Each non-Yearbook course offered at least once each period except lunch
    for course in set(courses).difference({"Yearbook"}):
        for period in set(periods).difference({"Lunch"}):
            print(cnf_output([[f(period, teacher, course, config) for teacher in teachers]]))

    # Yearbook is taught exactly once in periods 3 or 4
    print(cnf_output(exactly_1_true([
        f(period, teacher, "Yearbook", config)
        for (period, teacher) in product(["3", "4",], teachers)
    ])))

    # Mrs. A can't teach Yearbook
    is_this_printing = cnf_output([
        [-f(period, "Mrs. A", "Yearbook", config)]
        for period in periods
    ])
    print(is_this_printing)


    # No teacher teaches two courses in one period
    for period in periods:
        for teacher in teachers:
            for course_pair in combinations(courses, 2):
                print(
                    cnf_output(
                        [[-f(period, teacher, course_pair[0], config), -f(period, teacher, course_pair[1], config)]]
                    )
                )

    # Every teacher gets at least one non-lunch period off
    non_lunch = set(periods).difference({"Lunch"})

    def period_off_ands(teacher, period):
        return [
            -f(period, teacher, course, config)
            for course in courses
        ]

    for teacher in teachers:

        # p1:(-1^-2^-3) v p2:(-1^-2^-3) v ...
        ors_of_ands  = [
            period_off_ands(teacher, period)
            for period in non_lunch
        ]

        and_of_ors = and_of_ors_from_ors_of_ands(ors_of_ands)

        print(cnf_output(and_of_ors))

    # Nobody teaches during Lunch
    for tup in at_most_n_true(0, [
        f("Lunch", teacher, course, config)
        for (teacher, course) in product(teachers, courses)
    ]):
        print(cnf_output([tup]))


if __name__ == "__main__":
    main()
