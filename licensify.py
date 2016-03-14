#!/usr/bin/env python3

# Copyright 2016 Udey Rishi
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import argparse
import os
import sys
from licensors.licensor_factory import get_licensor


def main(arguments):
    licensor = get_licensor(arguments.license, arguments.path, arguments.project_name, arguments.owner,
                            arguments.recursive)
    modified_files, ignored_files = licensor.apply_license()

    print('Modified/Created files:')
    for file in modified_files:
        print(file)

    print(os.linesep + 'Ignored files because of unknown file extensions:')
    for file in ignored_files:
        print(file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='The path to the project root')
    parser.add_argument('project_name', help='The name of the project, as it should appear on the license')
    parser.add_argument('license', help='The name of the license. See config.py')
    parser.add_argument('owner', help='The owner of the project.')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='Enable complete stack trace for unhandled exceptions')
    parser.add_argument('-r', '--recursive', action='store_true',
                        help='Recursively travel inside the project root to apply the headers')
    args = parser.parse_args()

    try:
        main(args)
    except Exception as e:
        if args.debug:
            raise e
        else:
            print(e.__class__.__name__ + ': ' + str(e), file=sys.stderr)