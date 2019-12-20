#!/usr/bin/env python

import sys
import pytest
import importlib

BLACKLISTED_MODULE = 'lxml'


def secure_importer(name, globals=None, locals=None, fromlist=(), level=0):
    if name.startswith(BLACKLISTED_MODULE):
        raise ImportError("Cannot import module %s." % name)
    return importlib.__import__(name, globals, locals, fromlist, level)


def test_package_metadata():
    '''
    verify that the package metadata is available, even if no dependencies
    are installed.
    '''
    # clear the python search path to verify whether we can import
    # inscriptis even if its dependencies are not available
    # (required for building the docs and setup.py)
    saved_importer = __builtins__['__import__']
    saved_modules = {}
    with pytest.warns(UserWarning):
        # delete cached modules
        for module in list(sys.modules):
            if module.startswith('lxml') or module == 'inscriptis':
                saved_modules[module] = sys.modules[module]
                del sys.modules[module]

        # overwrite import mechanism
        __builtins__['__import__'] = secure_importer
        from inscriptis import (__version__, __author__, __author_email__,
                                __copyright__, __license__, __status__)

    assert __version__
    assert 'Albert' in __author__ and 'Fabian' in __author__
    assert '@fhgr' in __author_email__
    assert 'Albert' in __copyright__ and 'Fabian' in __copyright__
    assert 'GPL' in __license__
    assert __status__

    sys.modules.update(saved_modules)
    __builtins__['__import__'] = saved_importer
