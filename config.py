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


LANGUAGES = {
    # This dictionary contains all the supported languages, the comment patterns it uses, and the
    # corresponding file extensions. The list 'comment' should be either of size 1 or 2. Size 1
    # implies single-line comments (like // or #); size 2 implies block comments (like /* ... */).
    'C': {
        'comment': ['/**', '*/'],
        'extensions': ['.c', '.h']
    },
    'C++': {
        'comment': ['/**', '*/'],
        'extensions': ['.cc', '.cpp', '.cxx', '.c', '.c++', '.h', '.hh', '.hpp', '.hxx', '.h++']
    },
    'Java': {
        'comment': ['/**', '*/'],
        'extensions': ['.java']
    },
    'Python': {
        'comment': ['#'],
        'extensions': ['.py']
    },
    'C#': {
        'comment': ['/**', '*/'],
        'extensions': ['.cs']
    },
    'JavaScript': {
        'comment': ['/**', '*/'],
        'extensions': ['.js']
    },
    'Ada': {
        'comment': ['--'],
        'extensions': ['.adb', '.ads']
    },
    'AppleScript': {
        'comment': ['--'],
        'extensions': ['.scpt', '.AppleScript']
    },
    'BASIC': {
        'comment': ['REM'],
        'extensions': ['.bas', '.b']
    },
    'HTML': {
        'comment': ['<!--', '-->'],
        'extensions': ['.htm', '.html']
    },
    'XML': {
        'comment': ['<!--', '-->'],
        'extensions': ['.xml']
    },
    'Haskell': {
        'comment': ['{-', '-}'],
        'extensions': ['.hs']
    },
    'MATLAB': {
        'comment': ['%{', '%}'],
        'extensions': ['.m']
    },
    'Pascal': {
        'comment': ['[*', '*]'],
        'extensions': ['.p', '.pas', '.pl', '.pascal']
    },
    'Perl': {
        'comment': ['#'],
        'extensions': ['.pl']
    },
    'PHP': {
        'comment': ['/**', '*/'],
        'extensions': ['.php', '.php3', '.php4', '.php5', '.phps']
    },
    'PowerShell': {
        'comment': ['<#', '#>'],
        'extensions': ['.ps1']
    },
    'Ruby': {
        'comment': ['#'],
        'extensions': ['.rb']
    },
    'SQL': {
        'comment': ['--'],
        'extensions': ['.sql']
    },
    'TypeScript': {
        'comment': ['/**', '*/'],
        'extensions': ['.ts']
    },
    'Style': {
        'comment': ['/**', '*/'],
        'extensions': ['.css', '.less', '.sass', '.scss']
    },
    'Scala': {
        'comment': ['/**', '*/'],
        'extensions': ['.scala']
    }
}

LICENSES = {
    # This dictionary contains all the supported licenses (names are case-insenstive), and the
    # corresponding licensor class that does the work. See the licenses module for details.
    'ApacheV2': 'licenses.ApacheV2License',
    'MIT': 'licenses.MITLicense',
    'GPLV3': 'licenses.GPLV3License'
}
