#!/usr/bin/env python3

import argparse


def main(arguments):
    print(arguments.path)
    print(arguments.recursive)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help="The path to the project root")
    parser.add_argument("-r", "--recursive", action="store_true", help="Recursively travel inside the project root")
    args = parser.parse_args()
    main(args)
