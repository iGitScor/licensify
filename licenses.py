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


from abc import ABCMeta, abstractmethod
import os
import config
from datetime import datetime


COMMENT = 'comment'
EXTENSIONS = 'extensions'
SHE_BANG = '#!'

class LicenseNotSupportedError(Exception):
    pass


class LanguageNotSupportedError(Exception):
    pass


def get_first(collection, filter_func):
    for i in collection:
        if filter_func(i):
            return i

    return None


def get_licensor(license_name, root_path, project_name, owner, recursive=False):
    matched_license = get_first(config.LICENSES.items(), lambda l: l[0].lower().strip() == license_name.lower().strip())
    if matched_license is None:
        raise LicenseNotSupportedError("'{0}' license is not supported.".format(license_name))
    licensor = get_class(matched_license[1])
    return licensor(root_path, project_name, owner, recursive)


def get_class(kls):
    parts = kls.split('.')
    module = '.'.join(parts[:-1])
    m = __import__(module)
    for comp in parts[1:]:
        m = getattr(m, comp)
    return m


class License:
    __metaclass__ = ABCMeta

    def __init__(self, root_path, project_name, owner, recursive):
        self.root_path = root_path
        self.project_name = project_name
        self.owner = owner
        self.recursive = recursive

    @abstractmethod
    def apply_license(self):
        pass

    def write_files_to_root(self, files):
        created_files = []
        for file_name, contents in files.items():
            created_files.append(os.path.join(self.root_path, file_name))
            with open(created_files[-1], 'w') as file:
                file.write(contents)
        return created_files

    @classmethod
    def put_in_comment_block(cls, block, comment_style):
        if len(comment_style) is 1:
            # Single line comment style
            commented_header = ''
            for line in block.splitlines():
                commented_header += comment_style[0] + ' ' + line + os.linesep
            return commented_header
        else:
            # Multi-line comment style
            return '{0}{1}{2}{1}{3}'.format(comment_style[0], os.linesep,
                                            ' ' + block.replace(os.linesep, os.linesep + ' '),
                                            comment_style[1])

    @classmethod
    def get_commented_header(cls, header_contents, file_name):
        # If no file extension, treat the entire file name as extension (e.g: for Makefile)
        target_extension = file_name[max(0, max(file_name.rfind('.'), file_name.rfind(os.path.sep) + 1)):].strip()

        # Get first language that has the target_extension as one of the file extensions
        language = get_first(config.LANGUAGES.items(),
                             lambda lang: get_first(lang[1][EXTENSIONS],
                                                    lambda
                                                        extension: target_extension.strip() == extension.strip()) is not None)

        if language is None:
            raise LanguageNotSupportedError(
                    "Extension '{0}' for file '{1}' does not correspond to a supported programming language.".format(
                            target_extension, file_name))

        comment_style = language[1][COMMENT]
        return cls.put_in_comment_block(header_contents, comment_style)

    @staticmethod
    def prepend_header(header, file_contents):
        lines = file_contents.splitlines()
        shebang_index = 0
        for line in lines:
            if line.strip() == '':
                shebang_index += 1
            else:
                if line.strip().startswith(SHE_BANG):
                    lines.insert(shebang_index + 1, header)
                    return os.linesep.join(lines)
                else:
                    break
        return header + 2 * os.linesep + file_contents

    def apply_header(self, header_contents):
        ignored_files = []
        modified_files = []
        for root, _, files in os.walk(self.root_path):
            file_names = [os.path.join(root, f) for f in files]
            for filename in file_names:
                try:
                    commented_header = self.get_commented_header(header_contents, filename)
                except LanguageNotSupportedError:
                    ignored_files.append(filename)
                    continue

                with open(filename, 'r+') as f:
                    file_contents = f.read()
                    file_contents = self.prepend_header(commented_header, file_contents)
                    f.seek(0)
                    f.write(file_contents)
                    f.truncate()
                    modified_files.append(filename)

            if not self.recursive:
                break

        return modified_files, ignored_files


class ApacheV2License(License):
    TEMPLATE_DIR = 'templates/ApacheV2'
    LICENSE_FILE = 'LICENSE'
    NOTICE_FILE = 'NOTICE'
    YEAR_TEMPLATE = '{year}'
    OWNER_TEMPLATE = '{owner}'

    def __init__(self, root_path, project_name, owner, recursive):
        super().__init__(root_path, project_name, owner, recursive)

    def apply_license(self):
        with open(os.path.join(self.TEMPLATE_DIR, self.LICENSE_FILE), 'r') as license_file:
            license_contents = license_file.read()

        with open(os.path.join(self.TEMPLATE_DIR, self.NOTICE_FILE), 'r') as notice_file:
            notice_contents = notice_file.read() \
                .replace(self.YEAR_TEMPLATE, str(datetime.now().year)) \
                .replace(self.OWNER_TEMPLATE, self.owner)

        # Notice contents == header contents for Apache v2
        modified_files, ignored_files = self.apply_header(notice_contents)

        modified_files.extend(self.write_files_to_root({
            self.LICENSE_FILE: license_contents,
            self.NOTICE_FILE: notice_contents
        }))

        return modified_files, ignored_files


class GPLV3License(License):
    TEMPLATE_DIR = 'templates/GPLV3'
    LICENSE_FILE = 'LICENSE'
    HEADER_FILE = 'HEADER'
    YEAR_TEMPLATE = '{year}'
    OWNER_TEMPLATE = '{owner}'
    PROJECT_NAME_TEMPLATE = '{name}'

    def __init__(self, root_path, project_name, owner, recursive):
        super().__init__(root_path, project_name, owner, recursive)

    def apply_license(self):
        with open(os.path.join(self.TEMPLATE_DIR, self.HEADER_FILE), 'r') as header_file:
            header_contents = header_file.read() \
                .replace(self.YEAR_TEMPLATE, str(datetime.now().year)) \
                .replace(self.OWNER_TEMPLATE, self.owner) \
                .replace(self.PROJECT_NAME_TEMPLATE, self.project_name)

        modified_files, ignored_files = self.apply_header(header_contents)

        with open(os.path.join(self.TEMPLATE_DIR, self.LICENSE_FILE), 'r') as license_file:
            license_contents = license_file.read()

        modified_files.extend(self.write_files_to_root({self.LICENSE_FILE: license_contents}))

        return modified_files, ignored_files


class MITLicense(License):
    TEMPLATE_DIR = 'templates/MIT'
    LICENSE_FILE = 'LICENSE'
    YEAR_TEMPLATE = '{year}'
    OWNER_TEMPLATE = '{owner}'

    def __init__(self, root_path, project_name, owner, recursive):
        super().__init__(root_path, project_name, owner, recursive)

    def apply_license(self):
        year = str(datetime.now().year)
        header_contents = 'Copyright (c) {0} {1}. All rights reserved.'.format(year, self.owner)
        modified_files, ignored_files = self.apply_header(header_contents)

        with open(os.path.join(self.TEMPLATE_DIR, self.LICENSE_FILE), 'r') as license_file:
            license_contents = license_file.read() \
                .replace(self.YEAR_TEMPLATE, year) \
                .replace(self.OWNER_TEMPLATE, self.owner)

        modified_files.extend(self.write_files_to_root({self.LICENSE_FILE: license_contents}))

        return modified_files, ignored_files
