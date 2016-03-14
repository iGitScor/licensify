import config
from utils.collection_utils import get_first


class LicenseNotSupportedError(Exception):
    pass


def get_licensor(license_name, root_path, owner, recursive=False):
    matched_license = get_first(config.LICENSES.items(), lambda l: l[0].lower().strip() == license_name.lower().strip())
    if matched_license is None:
        raise LicenseNotSupportedError("'{0}' license is not supported.".format(license_name))
    licensor = get_class(matched_license[1])
    return licensor(root_path, owner, recursive)


def get_class(kls):
    parts = kls.split('.')
    module = ".".join(parts[:-1])
    m = __import__(module)
    for comp in parts[1:]:
        m = getattr(m, comp)
    return m
