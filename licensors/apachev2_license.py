import os

from licensors.license import License
from datetime import datetime


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
