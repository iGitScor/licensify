from abc import ABCMeta, abstractmethod


class License:
    __metaclass__ = ABCMeta

    def apply_license(self, path, recursive):
        print(self.NAME)
        print(path)
        print(recursive)


class ApacheV2License(License):
    NAME = 'ApacheV2'


class MITLicense(License):
    NAME = 'MIT'
