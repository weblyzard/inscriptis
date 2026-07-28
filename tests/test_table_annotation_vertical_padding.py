#!/usr/bin/env python

"""Regression tests for table cell annotation offsets in the presence of
vertical padding.

The multi-line ``TableCell.get_annotations`` path previously indexed
``annotation_lines`` by ``no + self.vertical_padding`` while iterating over
``line_break_pos`` built from the post-padded ``self.line_width``. That made
``no`` itself a padded line index, so the additional offset double-counted the
top padding and either crashed with ``IndexError`` (``valign=bottom``) or
silently shifted annotations onto padding lines (``valign=middle``).

Each test below forces real content lines (using ``<br>`` rather than block
elements that emit margin-empty-lines) so the padding/content distinction is
exercised cleanly.
"""

from inscriptis import get_annotated_text
from inscriptis.model.config import ParserConfig


def _annotated(html: str, rules: dict[str, list[str]]) -> dict:
    return get_annotated_text(html, ParserConfig(annotation_rules=rules))


def test_valign_bottom_indexerror_regression():
    """Reproduces the IndexError raised by inscriptis 2.7.3 when a cell with
    ``vertical-align: bottom`` is shorter than its row and contains
    annotations spanning multiple content lines.

    The short cell has 3 content lines vs. 10 in the sibling, forcing
    ``vertical_padding = 7``. Pre-fix, the second ``li`` annotation matches
    at padded index 7 and is then written to ``annotation_lines[7 + 7]``,
    overflowing the 10-entry list.
    """
    html = """
    <table>
      <tr>
        <td style="vertical-align:bottom">
          <ul><li>a1</li><li>a2</li><li>a3</li></ul>
        </td>
        <td>
          <ul>
            <li>b1</li><li>b2</li><li>b3</li><li>b4</li><li>b5</li>
            <li>b6</li><li>b7</li><li>b8</li><li>b9</li><li>b10</li>
          </ul>
        </td>
      </tr>
    </table>
    """
    # Pre-fix this raises IndexError; post-fix it returns successfully and
    # every left-column item is reachable via its ``li`` annotation slice.
    result = _annotated(html, {"li": ["li"]})

    li_slices = [result["text"][s:e] for s, e, t in result["label"] if t == "li"]
    for item in ("a1", "a2", "a3"):
        assert any(item in s for s in li_slices), f"{item!r} not covered: {li_slices}"


def test_valign_middle_multiline_annotation_offsets():
    """``valign=middle`` does not crash but silently places annotations on
    padding lines below the content. Cell has 3 content lines centered in a
    9-line row (top_pad=3, bottom_pad=3); annotations on the 2nd and 3rd
    content lines previously landed on padding lines 6 and 7 instead of
    content lines 4 and 5.
    """
    html = """
    <table>
      <tr>
        <td style="vertical-align:middle">
          <span>x1</span><br><span>x2</span><br><span>x3</span>
        </td>
        <td>L1<br>L2<br>L3<br>L4<br>L5<br>L6<br>L7<br>L8<br>L9</td>
      </tr>
    </table>
    """
    result = _annotated(html, {"span": ["s"]})

    span_slices = [result["text"][s:e] for s, e, t in result["label"] if t == "s"]
    # Pre-fix: ['x1 ', '3  ', ' L7']  (2nd/3rd shifted onto padding lines).
    # Post-fix: each span annotation must slice to its actual content.
    assert len(span_slices) == 3, f"expected 3 span annotations, got {span_slices}"
    assert "x1" in span_slices[0]
    assert "x2" in span_slices[1]
    assert "x3" in span_slices[2]


def test_valign_bottom_annotation_on_last_content_line():
    """A single annotation that starts on the last content line of a
    bottom-aligned cell must point at that content. Pre-fix the loop matches
    at padded index ``no = vertical_padding + rows - 1`` and the destination
    ``annotation_lines[2*vertical_padding + rows - 1]`` overflows for
    ``vertical_padding >= 1``.
    """
    html = """
    <table>
      <tr>
        <td style="vertical-align:bottom">
          first<br>second<br><b>third</b>
        </td>
        <td>L1<br>L2<br>L3<br>L4<br>L5<br>L6</td>
      </tr>
    </table>
    """
    result = _annotated(html, {"b": ["b"]})

    b = [a for a in result["label"] if a[2] == "b"]
    assert len(b) == 1
    start, end, _ = b[0]
    assert result["text"][start:end] == "third"


def test_padded_two_column_list():
    """Two columns of unequal height, so the shorter one is padded under the
    default ``valign=middle``. Every list item must be reachable via its
    annotation.
    """
    html = """
    <table>
      <tbody>
        <tr>
          <td>
            <ul><li>item1</li><li>item2</li></ul>
          </td>
          <td>
            <ul>
              <li>item5</li><li>item6</li><li>item7</li>
              <li>item8</li><li>item9</li><li>item10</li>
            </ul>
          </td>
        </tr>
      </tbody>
    </table>
    """
    result = _annotated(html, {"li": ["li"]})

    text = result["text"]
    li_slices = [text[s:e] for s, e, t in result["label"] if t == "li"]
    for item in ("item1", "item2", "item5", "item6", "item7", "item8", "item9", "item10"):
        assert any(item in s for s in li_slices), f"{item!r} missing: {li_slices}"
