from licensors.licensors import *
from utils.collection_utils import get_first


class LicenseNotSupportedError(Exception):
    pass


def get_licensor(license_name):
    licensor = get_first(License.__subclasses__(), lambda c: c.NAME.lower() == license_name.lower())
    if licensor is None:
        raise LicenseNotSupportedError("'{0}' license is not supported.".format(license_name))
    return licensor()
