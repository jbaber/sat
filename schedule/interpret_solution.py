#!/usr/bin/env python3

import sys
import re

def get_correspondence(filename):
    to_return = {}
    regex = re.compile(r'^c ([0-9]+): (.+) teaches (.+) period ([0-9]+)')
    with open(filename) as f:
        for line in f:
            maybe = regex.match(line)
            if maybe:
                to_return[int(maybe[1])] = {'teacher': maybe[2], 'course': maybe[3], 'period': int(maybe[4])}
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


def test_teachers_from_solution():
    correspondence = {
1: {'teacher': 'Mrs. A', 'course': 'English 9', 'period': 1},
2: {'teacher': 'Mr. B', 'course': 'English 9', 'period': 1},
3: {'teacher': 'Mrs. C', 'course': 'English 9', 'period': 1}
}
    assert teachers_from_solution(1, "English 9", [1], correspondence) == ["Mrs. A",]
    assert teachers_from_solution(1, "English 9", [1, 2], correspondence) == ["Mrs. A", "Mr. B"]
    assert teachers_from_solution(1, "English 10", [1, 2], correspondence) == []


def teachers_from_correspondence(correspondence):
    return set([
        correspondence[key]["teacher"]
        for key in correspondence
    ])


def courses_from_correspondence(correspondence):
    return set([
        correspondence[key]["course"]
        for key in correspondence
    ])


def periods_from_correspondence(correspondence):
    return set([
        int(correspondence[key]["period"])
        for key in correspondence
    ])


def teachers_from_solution(period, course, solution, correspondence):
    return [
        correspondence[key]["teacher"]
        for key in solution
        if correspondence[key]["period"] == period
        and correspondence[key]["course"] == course
    ]


def plot_solution(solution, correspondence):
    periods = periods_from_correspondence(correspondence)
    courses = courses_from_correspondence(correspondence)

    to_return = "<html><body><table>\n<tr>"
    to_return += "<th>&nbsp;</th>"
    for period in periods:
        to_return += f"<th>{period}</th>"
    to_return += "</tr>\n"

    for course in courses:
        to_return += f"<tr><td>{course}</td>"
        for period in periods:
            to_return += "<td>"
            them = teachers_from_solution(period, course, solution, correspondence)
            to_return += ",".join(them)
            to_return += "</td>"
        to_return += "</tr>\n"
    to_return += "</table></body></html>"

    return to_return



    for facet in solution:
        c = correspondence[facet]
        to_return += f"{c['teacher']} teaches {c['course']} period {c['period']}\n"

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
