#!/usr/bin/env python
# encoding: utf-8

"""
Tests the rendering of a single table line.
"""

from inscriptis.model.canvas import Prefix


def test_simple_prefix_iterator():
    p = Prefix()

    p.register_prefix(5, '1. ')

    for no, line in enumerate(p):
        if no == 0:
            assert line == '  1. '
        else:
            assert line == '     '

        if no > 10:
            break

def test_combined_prefix_iterator():
    p = Prefix()

    p.register_prefix(5, '1. ')
    p.register_prefix(2, '')

    # first consumption - should yield the bullet
    for no, line in enumerate(p):
        if no == 0:
            assert line == '    1. '
        else:
            assert line == '       '

        if no > 10:
            break

    # the first consumption hasn't been successful
    # restore the last state
    p.restore()
    for no, line in enumerate(p):
        if no == 0:
            assert line == '    1. '
        else:
            assert line == '       '

        if no > 10:
            break


    # another consumption - the bullet is gone
    for no, line in enumerate(p):
        assert line == '       '

        if no > 10:
            break

    p.remove_last_prefix()
    # second consumption - without the bullet
    for no, line in enumerate(p):
        assert line == '     '
        if no > 2:
            break

    p.remove_last_prefix()
    # final consumption - no prefix
    for no, line in enumerate(p):
        assert line == ''
        if no > 2:
            break

    # ensure that there are no interactions between different runs with
    # bullets
    p.register_prefix(5, '2. ')
    p.register_prefix(2, '- ')

    for no, line in enumerate(p):
        if no == 0:
            assert line == '    2. '
        else:
            assert line == '       '

        if no > 2:
            break

    for no, line in enumerate(p):
        if no == 0:
            assert line == '     - '
        else:
            assert line == '       '

        if no > 2:
            break

