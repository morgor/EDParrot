#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to build to .exe and .msi package.
.exe build is via py2exe on win32.
.msi packaging utilises Windows SDK.
"""

import codecs
import os
import platform
import re
import shutil
import sys
from distutils.core import setup
from os.path import exists, isdir, join
from tempfile import gettempdir
from typing import Any, Generator, Set

from config import (
    appcmdname, applongname, appname, appversion, appversion_nobuild, copyright, git_shorthash_from_head, update_feed,
    update_interval
)
from constants import GITVERSION_FILE

if sys.version_info[0:2] != (3, 9):
    raise AssertionError(f'Unexpected python version {sys.version}')

###########################################################################
# Retrieve current git short hash and store in file GITVERSION_FILE
git_shorthash = git_shorthash_from_head()
if git_shorthash is None:
    exit(-1)

with open(GITVERSION_FILE, 'w+', encoding='utf-8') as gvf:
    gvf.write(git_shorthash)

print(f'Git short hash: {git_shorthash}')
###########################################################################

if sys.platform == 'win32':
    assert platform.architecture()[0] == '32bit', 'Assumes a Python built for 32bit'
    import py2exe  # noqa: F401 # Yes, this *is* used
    dist_dir = 'dist.win32'

elif sys.platform == 'darwin':
    dist_dir = 'dist.macosx'

else:
    assert False, f'Unsupported platform {sys.platform}'

# Split version, as py2exe wants the 'base' for version
semver = appversion()
appversion_str = str(semver)
base_appversion = str(semver.truncate('patch'))

if dist_dir and len(dist_dir) > 1 and isdir(dist_dir):
    shutil.rmtree(dist_dir)

# "Developer ID Application" name for signing
macdeveloperid = None

# Windows paths
WIXPATH = r'C:\Program Files (x86)\WiX Toolset v3.11\bin'
SDKPATH = r'C:\Program Files (x86)\Windows Kits\10\bin\10.0.19041.0\x86'

# OSX paths
SPARKLE = '/Library/Frameworks/Sparkle.framework'

if sys.platform == 'darwin':
    # Patch py2app recipe enumerator to skip the sip recipe since it's too
    # enthusiastic - we'll list additional Qt modules explicitly
    import py2app.build_app
    from py2app import recipes

    # NB: 'Any' is because I don't have MacOS docs
    def iter_recipes(module=recipes) -> Generator[str, Any]:
        """Enumerate recipes via alternate method."""
        for name in dir(module):
            if name.startswith('_') or name == 'sip':
                continue
            check = getattr(getattr(module, name), 'check', None)
            if check is not None:
                yield (name, check)

    py2app.build_app.iterRecipes = iter_recipes


APP = 'EDParot.py'
APPCMD = 'EDParot.py'
SND = [
    'snd/snd1.wav',
    'snd/snd2.wav',
    'snd/snd3.wav',
    'snd/snd4.wav',
    'snd/snd5.wav',
    'snd/snd6.wav',
]

if sys.platform == 'win32':
    OPTIONS = {
        'py2exe': {
            'dist_dir': dist_dir,
            'optimize': 2,
            'packages': [
                'sqlite3',  # Included for plugins
            ],
            'includes': [
                'dataclasses',
                'shutil',  # Included for plugins
                'timeout_session',
                'zipfile',  # Included for plugins
            ],
            'excludes': [
                'distutils',
                '_markerlib',
                'optparse',
                'PIL',
                'simplejson',
                'unittest'
            ],
        }
    }

    DATA_FILES = [
        ('', [
            'requirements.txt',  # Contains git short hash
            'README.md',
        ]),
        ('snd', SND),
    ]

setup(
    name=applongname,
    version=appversion_str,
    windows=[
        {
            'dest_base': appname,
            'script': APP,
            'icon_resources': [(0, f'{appname}.ico')],
            'company_name': 'EDCD',  # Used by WinSparkle
            'product_name': appname,  # Used by WinSparkle
            'version': base_appversion,
            'product_version': appversion_str,
            'copyright': copyright,
            'other_resources': [(24, 1, open(f'{appname}.manifest').read())],
        }
    ],
    console=[
        {
            'dest_base': appcmdname,
            'script': APPCMD,
            'company_name': 'EDCD',
            'product_name': appname,
            'version': base_appversion,
            'product_version': appversion_str,
            'copyright': copyright,
            'other_resources': [(24, 1, open(f'{appcmdname}.manifest').read())],
        }
    ],
    data_files=DATA_FILES,
    options=OPTIONS,
)

package_filename = None
if sys.platform == 'win32':
    os.system(rf'"{WIXPATH}\candle.exe" -out {dist_dir}\ {appname}.wxs')

    if not exists(f'{dist_dir}/{appname}.wixobj'):
        raise AssertionError(f'No {dist_dir}/{appname}.wixobj: candle.exe failed?')

    package_filename = f'{appname}_win_{appversion_nobuild()}.msi'
    os.system(rf'"{WIXPATH}\light.exe" -sacl -spdb -sw1076 {dist_dir}\{appname}.wixobj -out {package_filename}')

    if not exists(package_filename):
        raise AssertionError(f'light.exe failed, no {package_filename}')

    # Seriously, this is how you make Windows Installer use the user's display language for its dialogs. What a crock.
    # http://www.geektieguy.com/2010/03/13/create-a-multi-lingual-multi-language-msi-using-wix-and-custom-build-scripts
    lcids = [
        int(x) for x in re.search(  # type: ignore
            r'Languages\s*=\s*"(.+?)"',
            open(f'{appname}.wxs').read()
        ).group(1).split(',')
    ]
    assert lcids[0] == 1033, f'Default language is {lcids[0]}, should be 1033 (en_US)'
    shutil.copyfile(package_filename, join(gettempdir(), f'{appname}_1033.msi'))
    for lcid in lcids[1:]:
        shutil.copyfile(
            join(gettempdir(), f'{appname}_1033.msi'),
            join(gettempdir(), f'{appname}_{lcid}.msi')
        )
        # Don't care about codepage because the displayed strings come from msiexec not our msi
        os.system(rf'cscript /nologo "{SDKPATH}\WiLangId.vbs" {gettempdir()}\{appname}_{lcid}.msi Product {lcid}')
        os.system(rf'"{SDKPATH}\MsiTran.Exe" -g {gettempdir()}\{appname}_1033.msi {gettempdir()}\{appname}_{lcid}.msi {gettempdir()}\{lcid}.mst')  # noqa: E501 # Not going to get shorter
        os.system(rf'cscript /nologo "{SDKPATH}\WiSubStg.vbs" {package_filename} {gettempdir()}\{lcid}.mst {lcid}')

else:
    raise AssertionError('Unsupported platform')
