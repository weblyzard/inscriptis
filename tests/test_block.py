"""
Test cases for the Block class.
"""

from inscriptis.model.canvas.block import Block
from inscriptis.model.canvas.prefix import Prefix


def test_merge_normal_text_collapsable_whitespaces():
    """
    test cases where the block has collapsable whitespaces
    """
    b = Block(0, Prefix())
    b.merge_normal_text("Hallo")
    assert b._content == "Hallo"
    assert not b.collapsable_whitespace

    b = Block(0, Prefix())
    b.merge_normal_text(" Hallo ")
    assert b._content == "Hallo "
    assert b.collapsable_whitespace

    b = Block(0, Prefix())
    b.merge_normal_text("")
    assert b._content == ""
    assert b.collapsable_whitespace

    b.merge_normal_text(" ")
    assert b._content == ""
    assert b.collapsable_whitespace

    b.merge_normal_text("  ")
    assert b._content == ""
    assert b.collapsable_whitespace


def test_merge_normal_non_collapsable_whitespaces():
    b = Block(0, Prefix())
    b.collapsable_whitespace = False
    b.merge_normal_text("Hallo")
    assert b._content == "Hallo"
    assert not b.collapsable_whitespace

    b = Block(0, Prefix())
    b.collapsable_whitespace = False
    b.merge_normal_text(" Hallo ")
    assert b._content == " Hallo "
    assert b.collapsable_whitespace

    b = Block(0, Prefix())
    b.collapsable_whitespace = False
    b.merge_normal_text("")
    assert b._content == ""
    assert not b.collapsable_whitespace

    b = Block(0, Prefix())
    b.collapsable_whitespace = False
    b.merge_normal_text(" ")
    assert b._content == " "
    assert b.collapsable_whitespace

    b = Block(0, Prefix())
    b.collapsable_whitespace = False
    b.merge_normal_text("  ")
    assert b._content == " "
    assert b.collapsable_whitespace
