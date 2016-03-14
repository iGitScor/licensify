from abc import ABCMeta, abstractmethod
import os
from utils.collection_utils import get_first
import config

COMMENT = 'comment'
EXTENSIONS = 'extensions'
SHE_BANG = '#!'


class LanguageNotSupportedError(Exception):
    pass


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

    @staticmethod
    def write_files(files):
        for file_name, contents in files.items():
            with open(file_name, 'w') as file:
                file.write(contents)

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
                    lines.insert(shebang_index + 1, 2 * os.linesep + header + 2 * os.linesep)
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
                with open(filename, 'r+') as f:
                    file_contents = f.read()
                    try:
                        commented_header = self.get_commented_header(header_contents, filename)
                    except LanguageNotSupportedError:
                        ignored_files.append(filename)
                        continue
                    file_contents = self.prepend_header(commented_header, file_contents)
                    f.seek(0)
                    f.write(file_contents)
                    f.truncate()
                    modified_files.append(filename)

            if not self.recursive:
                break

        return modified_files, ignored_files
