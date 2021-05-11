#!/usr/bin/env python3

import sys


def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <original.cnf> <extra-conditions.txt>")
        exit(1)

    with open(sys.argv[2]) as f:
        for line in f:
            print(line)

if __name__ == "__main__":
    main()
