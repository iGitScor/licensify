from licensors.licensors import License


class MITLicense(License):
    def __init__(self, root_path, owner, recursive):
        super().__init__(root_path, owner, recursive)

    def apply_license(self):
        return [], []
