import os

from licensors.licensors import License
from datetime import datetime


class ApacheV2License(License):
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

        modified_files, ignored_files = self.apply_header(notice_contents)

        license_file_path = os.path.join(self.root_path, self.LICENSE_FILE)
        notice_file_path = os.path.join(self.root_path, self.NOTICE_FILE)
        self.write_files({
            license_file_path: license_contents,
            notice_file_path: notice_contents
        })

        modified_files.append(license_file_path)
        modified_files.append(notice_file_path)
        return modified_files, ignored_files
