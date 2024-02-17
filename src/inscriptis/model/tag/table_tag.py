"""Handle the <table>, <tr> and <td> tags."""
from typing import Dict

from inscriptis.annotation import Annotation
from inscriptis.model.canvas import Canvas
from inscriptis.model.html_document_state import HtmlDocumentState
from inscriptis.model.table import Table, TableCell


def td_start_handler(state: HtmlDocumentState, _: Dict) -> None:
    """Handle the <td> tag."""
    if state.current_table:
        # open td tag
        table_cell = TableCell(align=state.tags[-1].align, valign=state.tags[-1].valign)
        state.tags[-1].canvas = table_cell
        state.current_table[-1].add_cell(table_cell)


def tr_start_handler(state: HtmlDocumentState, _: Dict) -> None:
    """Handle the <tr> tag."""
    if state.current_table:
        state.current_table[-1].add_row()


def table_start_handler(state: HtmlDocumentState, _: Dict) -> None:
    """Handle the <table> tag."""
    state.tags[-1].set_canvas(Canvas())
    state.current_table.append(
        Table(
            left_margin_len=state.tags[-1].canvas.left_margin,
            cell_separator=state.config.table_cell_separator,
        )
    )


def td_end_handler(state: HtmlDocumentState) -> None:
    """Handle the </td> tag."""
    if state.current_table:
        state.tags[-1].canvas.close_tag(state.tags[-1])


def table_end_handler(state: HtmlDocumentState) -> None:
    """Handle the </table> tag."""
    if state.current_table:
        td_end_handler(state)
    table = state.current_table.pop()
    # last tag before the table: self.tags[-2]
    # table tag: self.tags[-1]

    out_of_table_text = state.tags[-1].canvas.get_text().strip()
    if out_of_table_text:
        state.tags[-2].write(out_of_table_text)
        state.tags[-2].canvas.write_newline()

    start_idx = state.tags[-2].canvas.current_block.idx
    state.tags[-2].write_verbatim_text(table.get_text())
    state.tags[-2].canvas.flush_inline()

    # transfer annotations from the current tag
    if state.tags[-1].annotation:
        end_idx = state.tags[-2].canvas.current_block.idx
        for a in state.tags[-1].annotation:
            state.tags[-2].canvas.annotations.append(Annotation(start_idx, end_idx, a))

    # transfer in-table annotations
    state.tags[-2].canvas.annotations.extend(
        table.get_annotations(start_idx, state.tags[-2].canvas.left_margin)
    )
