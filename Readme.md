##Licensify

Licensify is an app for adding licenses to projects. Features include:

1. adding license header stubs to all of your source code files
2. adding license/notice files in the root directory

Licensify works with multiple programming languages; and can thus, be incorporated into a wide variety of projects. It currently supports the MIT License, Apache V2, and GPL V3.

Licensify is flexible, so it can be extended according to need. You can easily add support for other file formats and licenses. Remember to send a PR, so that everyone can benefit! :smile:

###Usage
```sh
$ python3 licensify.py /path/to/project_root "My Great App" apachev2 "Udey Rishi" -r

# For help
$ python3 licensify.py --help
```

See the ```LICENSES``` dictionary in ```config.py``` for all the supported licenses (case insensitive). The ```-r``` option recursively licensifies all the subdirectories in the root; omit it if that's not desired.

###Adding Language Support

1. Change the ```LANGUAGES``` dictionary in ```config.py``` appropriately. Each language should have the corresponding ```comment``` and ```extensions``` lists to specify the comment styles, and the source code file formats for that language, respectively.
2. If a single element is present in the ```comment``` list, then that element is used for generating line comments for the license headers.
3. If two elements are present in the ```comment``` list, then these elements are used for generating block comments for the license headers.

###Adding License Support

1. Every license generation class should meet the the following API:
	* A constructor that takes these arguments: ```(root_path: str, project_name: str, owner: str, recursive: bool)```
	* The method ```apply_license()``` that applies the license.
	* A key-value pair be added to the ```LICENSES``` dictionary in ```config.py``` so that the factory can see it.

	It is recommended that the new class extends the ```licensors.license.License``` class, as it provides some useful methods. See the existing subclasses for guidance.
