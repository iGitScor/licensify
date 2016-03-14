import os
from datetime import datetime

from licensors.license import License


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
