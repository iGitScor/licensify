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
