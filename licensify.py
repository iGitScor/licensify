#!/usr/bin/env python3

import argparse
import sys
from licensors.licensor_factory import get_licensor


def main(arguments):
    licensor = get_licensor(arguments.license)
    licensor.apply_license(arguments.path, arguments.recursive)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='The path to the project root')
    parser.add_argument('license', help='The name of the license. See config.py')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='Enable complete stack trace for unhandled exceptions')
    parser.add_argument('-r', '--recursive', action='store_true', help='Recursively travel inside the project root')
    args = parser.parse_args()

    try:
        main(args)
    except Exception as e:
        if args.debug:
            raise e
        else:
            print(e, file=sys.stderr)
