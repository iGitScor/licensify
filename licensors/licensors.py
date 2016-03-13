from abc import ABCMeta, abstractmethod
import os
import sys
from datetime import datetime
from utils.collection_utils import get_first
import config


class LanguageNotSupportedError(Exception):
    pass


class License:
    __metaclass__ = ABCMeta

    def __init__(self, root_path, owner, recursive):
        self.root_path = root_path
        self.owner = owner
        self.recursive = recursive

    @abstractmethod
    def apply_license(self):
        pass

    def write_files(self, files):
        for file_name, contents in files.items():
            file_path = os.path.join(self.root_path, file_name)
            with open(file_path, 'w') as file:
                file.write(contents)

    @staticmethod
    def __match_extension(target_extension, language_extensions_pair):
        target_extension = target_extension.strip()
        if type(language_extensions_pair[1]) is str:
            ext = language_extensions_pair[1]
            return target_extension == ext.strip()
        elif len(language_extensions_pair) is 1:
            ext = language_extensions_pair[1][0]
            return target_extension == ext.strip()
        else:
            return get_first(language_extensions_pair[1], lambda x: target_extension == x.strip()) is not None

    @classmethod
    def put_in_comment_block(cls, block, language):
        if language not in config.COMMENT_STYLES:
            raise ValueError("Language '{0}''s comment style not defined in config.COMMENT_STYLES".format(language))

        comment_style = config.COMMENT_STYLES[language]
        if type(comment_style) == str:
            # Single line comment style
            commented_header = ''
            for line in block.splitlines():
                commented_header += comment_style + ' ' + line + os.linesep
            return commented_header
        else:
            # Multi-line comment style
            return '{0}{1}{2}{1}{3}'.format(comment_style[0], os.linesep, block, comment_style[1])

    @classmethod
    def get_commented_header(cls, header_contents, file_name):
        # If no file extension, treat the entire file name as extension (e.g: for Makefile)
        target_extension = file_name[max(0, max(file_name.rfind('.'), file_name.rfind(os.path.sep) + 1)):].strip()
        language_ext_pair = get_first(config.FILE_EXTENSIONS.items(),
                                      lambda ext: cls.__match_extension(target_extension, ext))
        if language_ext_pair is None:
            raise LanguageNotSupportedError(file_name)

        return cls.put_in_comment_block(header_contents, language_ext_pair[0])

    def apply_header(self, header_contents):
        ignored_files = []
        for root, _, files in os.walk(self.root_path):
            file_names = [os.path.join(root, f) for f in files]
            for filename in file_names:
                with open(filename, 'r+') as f:
                    file_contents = f.read()
                    try:
                        commented_header = self.get_commented_header(header_contents, filename)
                    except LanguageNotSupportedError as e:
                        ignored_files.append(str(e))
                        continue
                    file_contents = commented_header + os.linesep + os.linesep + file_contents
                    f.seek(0)
                    f.write(file_contents)
                    f.truncate()

            if not self.recursive:
                break

        return ignored_files


class ApacheV2License(License):
    NAME = 'ApacheV2'
    TEMPLATE_DIR = 'templates/ApacheV2'
    LICENSE_FILE = 'LICENSE'
    NOTICE_FILE = 'NOTICE'
    YEAR_TEMPLATE = '{year}'
    OWNER_TEMPLATE = '{owner}'

    def __init__(self, root_path, owner, recursive):
        super().__init__(root_path, owner, recursive)

    def apply_license(self):
        with open(os.path.join(self.TEMPLATE_DIR, self.LICENSE_FILE), 'r') as license_file:
            license_contents = license_file.read()

        with open(os.path.join(self.TEMPLATE_DIR, self.NOTICE_FILE), 'r') as notice_file:
            notice_contents = notice_file.read() \
                .replace(self.YEAR_TEMPLATE, str(datetime.now().year)) \
                .replace(self.OWNER_TEMPLATE, self.owner)

        ignored_files = self.apply_header(notice_contents)

        if len(ignored_files) > 0:
            print('Ignoring these files because of unknown file extension:', file=sys.stderr)
            for file in ignored_files:
                print(file, file=sys.stderr)

        self.write_files({
            self.LICENSE_FILE: license_contents,
            self.NOTICE_FILE: notice_contents
        })


class MITLicense(License):
    NAME = 'MIT'

    def __init__(self, root_path, owner, recursive):
        super().__init__(root_path, owner, recursive)

    def apply_license(self):
        pass
