#!/usr/bin/env python

import sys
import pytest


def test_package_metadata():
    '''
    verify that the package metadata is available, even if no dependencies
    are installed.
    '''
    # clear the python search path to verify whether we can import
    # inscriptis even if its dependencies are not available
    # (required for building the docs and setup.py)
    with pytest.warns(UserWarning):
        syspath = sys.path.copy()
        sys.path = [path for path in sys.path if '/inscriptis/' in path]

        # delete cached modules
        saved = {}
        for module in list(sys.modules):
            if module.startswith('lxml') or module == 'inscriptis':
                saved[module] = sys.modules[module]
                del sys.modules[module]

        from inscriptis import (__version__, __author__, __author_email__,
                                __copyright__, __license__, __status__)

    assert __version__
    assert 'Albert' in __author__ and 'Fabian' in __author__
    assert '@fhgr' in __author_email__
    assert 'Albert' in __copyright__ and 'Fabian' in __copyright__
    assert 'GPL' in __license__
    assert __status__

    sys.modules.update(saved)
    sys.path = syspath
