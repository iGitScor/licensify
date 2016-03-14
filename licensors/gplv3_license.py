import os
from datetime import datetime

from licensors.license import License


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
