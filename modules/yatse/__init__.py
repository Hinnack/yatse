# -*- coding: utf-8 -*-
from django.conf import settings
from sys import version_info

version = '@version@'

if 'version' in version:
    VERSION = ('a', 'b', 'c', '', 0)
else:
    VERSION = version.split('.')
    VERSION.append('')
    VERSION.append(0)

def get_version():
    version = '%s.%s' % (VERSION[0], VERSION[1])
    if VERSION[2]:
        version = '%s.%s' % (version, VERSION[2])
    if VERSION[3:] == ('alpha', 0):
        version = '%s pre-alpha' % version
    else:
        if VERSION[3] != 'final':
            version = '%s %s %s' % (version, VERSION[3], VERSION[4])
    return version

def get_python_version():
    version = '%s.%s' % (version_info[0], version_info[1])
    if version_info[2]:
        version = '%s.%s' % (version, version_info[2])
    if version_info[3:] == ('alpha', 0):
        version = '%s pre-alpha' % version
    else:
        if version_info[3] != 'final':
            version = '%s %s %s' % (version, version_info[3], version_info[4])
    return version
