## Licensify

Licensify makes adding licenses to your projects a breeze. It automatically adds the license/notice files in the root directory of your project, and adds the copyright headers to all your source files. It supports multiple languages (identified by the file extensions), and supports MIT, Apache V2, and GPL V3 licenses out of the box.

### Usage
```sh
$ ./licensify.py -h
usage: licensify.py [-h] [-d] [-r] path project_name license owner

positional arguments:
  path             The path to the project root
  project_name     The name of the project, as it should appear on the license
  license          The name of the license. See config.py
  owner            The owner of the project.

optional arguments:
  -h, --help       show this help message and exit
  -d, --debug      Enable complete stack trace for unhandled exceptions
  -r, --recursive  Recursively travel inside the project root to apply the
                   headers
```

See the `LANGUAGES` and `LICENSES` dictionaries in `config.py` for all the supported languages and licenses, respectively.

### Adding Language Support

* Add an entry to the `LANGUAGES` dictionary in `config.py`.

### Adding License Support

Every license generation class should meet the the following API:

* A constructor that takes these arguments: ```(root_path: str, project_name: str, owner: str, recursive: bool)```
* The method ```apply_license()``` that applies the license. This method should return two lists: (i) the modified/created files, and (ii) ignored files (unknown file extensions, etc.).

Additionally, a key-value pair needs to be added to the `LICENSES` dictionary in `config.py` so that the factory can see it.

It is recommended that the new class extends the `licenses.License` class, as it provides some useful methods. See the existing subclasses for guidance.
