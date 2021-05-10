#!/usr/bin/env python3

from itertools import combinations
from itertools import product

PERIODS = (1, 2, 3)
TEACHERS = ("Mrs. A", "Mr. B", "Mrs. C")
COURSES = ("English 9", "English 10", "English 11")

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
def var_from_period_teacher_course(period, teacher, course):
    if teacher not in TEACHERS:
        raise ValueError(f"{teacher} not in  {TEACHERS}")
    if period not in PERIODS:
        raise ValueError(f"{period} not in {PERIODS}")
    if course not in COURSES:
        raise ValueError(f"{course} not in {COURSES}")

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



def cnf_output(clauses):
    to_return = []
    for clause in clauses:
        to_return.append(" ".join(str(x) for x in clause) + " 0")
    return "\n".join(to_return)


def main():

    # Each course offered at least once each period
    for course in COURSES:
        for period in PERIODS:
            print(cnf_output([[f(period, teacher, course) for teacher in TEACHERS]]))

    #  # No teacher teaches two courses in one period
    #  for period in PERIODS:
    #      for teacher in TEACHERS:
    #          for course_pair in combinations(COURSES, 2):
    #              print(
    #                  cnf_output(
    #                      [[-f(period, teacher, course_pair[0]), -f(period, teacher, course_pair[1])]]
    #                  )
    #              )

    #  # Every teacher gets at least one period off
    #  for teacher in TEACHERS:
    #      rows = [[-f(period, teacher, course) for course in COURSES] for period in PERIODS]
    #      for tup in product(*rows):
    #          print(cnf_output([tup]))


if __name__ == "__main__":
    main()
