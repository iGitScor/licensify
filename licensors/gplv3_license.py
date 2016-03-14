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
        year = str(datetime.now().year)
        with open(os.path.join(self.TEMPLATE_DIR, self.HEADER_FILE), 'r') as header_file:
            header_contents = header_file.read() \
                .replace(self.YEAR_TEMPLATE, year) \
                .replace(self.OWNER_TEMPLATE, self.owner) \
                .replace(self.PROJECT_NAME_TEMPLATE, self.project_name)

        modified_files, ignored_files = self.apply_header(header_contents)

        with open(os.path.join(self.TEMPLATE_DIR, self.LICENSE_FILE), 'r') as license_file:
            license_contents = license_file.read()

        license_file_path = os.path.join(self.root_path, self.LICENSE_FILE)
        self.write_files({license_file_path: license_contents})
        modified_files.append(license_file_path)

        return modified_files, ignored_files
