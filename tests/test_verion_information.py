#!/usr/bin/env python

import os
import sys


def test_package_metadata():
    '''
    verify that the package metadata is available, even if no dependencies
    are installed.
    '''
    # clear the python search path to verify whether we can import
    # inscriptis even if its dependencies are not available
    # (required for building the docs and setup.py)
    syspath = sys.path.copy()
    sys.path.clear()
    sys.path.append(os.path.join(os.getcwd(), '../src'))

    from inscriptis import (__version__, __author__, __author_email__,
                            __copyright__, __license__, __status__)

    assert __version__
    assert 'Albert' in __author__ and 'Fabian' in __author__
    assert '@fhgr' in __author_email__
    assert 'Albert' in __copyright__ and 'Fabian' in __copyright__
    assert 'GPL' in __license__
    assert __status__

    sys.path = syspath
