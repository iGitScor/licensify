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


import config
from utils.collection_utils import get_first


class LicenseNotSupportedError(Exception):
    pass


def get_licensor(license_name, root_path, project_name, owner, recursive=False):
    matched_license = get_first(config.LICENSES.items(), lambda l: l[0].lower().strip() == license_name.lower().strip())
    if matched_license is None:
        raise LicenseNotSupportedError("'{0}' license is not supported.".format(license_name))
    licensor = get_class(matched_license[1])
    return licensor(root_path, project_name, owner, recursive)


def get_class(kls):
    parts = kls.split('.')
    module = ".".join(parts[:-1])
    m = __import__(module)
    for comp in parts[1:]:
        m = getattr(m, comp)
    return m
