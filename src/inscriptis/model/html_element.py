from inscriptis.html_properties import Display, HorizontalAlignment, VerticalAlignment, WhiteSpace


class HtmlElement:
    """
    The HtmlElement class stores the following CSS properties of HTML
    elements:

    - tag: tag name of the given HtmlElement.
    - prefix: specifies a prefix that to insert before the tag's content.
    - suffix: a suffix to append after the tag's content.
    - display: :class:`~inscriptis.html_properties.Display` strategy used for
      the content.
    - margin_before: vertical margin before the tag's content.
    - margin_after: vertical margin after the tag's content.
    - padding: horizontal padding before the tag's content.
    - whitespace: the :class:`~inscriptis.html_properties.Whitespace` handling
      strategy.
    - limit_whitespace_affixes: limit printing of whitespace affixes to
      elements with `normal` whitespace handling.
    """

    __slots__ = ('canvas', 'tag', 'prefix', 'suffix', 'display',
                 'margin_before', 'margin_after', 'padding', 'list_bullet',
                 'whitespace', 'limit_whitespace_affixes', 'align', 'valign',
                 'is_empty')

    def __init__(self, tag='default', prefix='', suffix='', display=Display.inline,
                 margin_before=0, margin_after=0, padding=0, list_bullet='',
                 whitespace=None, limit_whitespace_affixes=False,
                 align=HorizontalAlignment.left,
                 valign=VerticalAlignment.middle):
        self.canvas = None
        self.tag = tag
        self.prefix = prefix
        self.suffix = suffix
        self.display = display
        self.margin_before = margin_before
        self.margin_after = margin_after
        self.padding = padding
        self.list_bullet = list_bullet
        self.whitespace = whitespace
        self.limit_whitespace_affixes = limit_whitespace_affixes
        self.align = align
        self.valign = valign
        self.is_empty = True       # whether this is an empty element

    def write(self, text):
        """
        Writes the given HTML text.
        """
        if not (text and not text.isspace()):
            return

        self.is_empty = False
        HtmlElement.WRITER[self.display](self, text)

    def write_tail(self, text, is_close_block):
        """
        Writes the tail text of an element.

        Args:
            text: the text to write
            is_close_block: whether the given text follows the end of a block
                            elements.
        """
        if not text:
            return

        if self.display == Display.block and is_close_block:
            print("AFTER")
            self.canvas.write_block(self, '\n' * self.margin_after + ' ' * self.padding)
        self.write_inline_text(text)

    def set_canvas(self, canvas):
        self.canvas = canvas
        return self

    def set_tag(self, tag):
        self.tag = tag
        return self

    def write_inline_text(self, text):
        """
        Writes floating HTML text. All whitespaces are collapsed.
        Args:
            text: the text to write
        """
        self.canvas.write_inline(self,
                                 ''.join((self.prefix, text, self.suffix)))

    def write_block_text(self, text):
        """
        Writes floating HTML text. All whitespaces are collapsed.
        Args:
            text: the text to write
        """
        self.canvas.flush_inline()
        self.canvas.blocks.append('\n' * self.margin_before)
        self.canvas.write_block(self, ''.join(
            (
                self.prefix,
                text.lstrip(),
                self.suffix
            )
        ))

    def write_display_none(self, text):
        return

    def write_verbatim_text(self, text):
        """
        Writes the given text verbatim to the canvas.
        Args:
            text: the text to write
        """
        if not text:
            return
        base_padding = ' ' * self.padding
        self.canvas.write_block(self, text.replace('\n', '\n' + base_padding))

    def close_block(self):
        """
        Closes a block in the canvas
        """
        self.canvas.flush_inline()

    def get_refined_html_element(self, new):
        """
        Computes the new HTML element based on the previous one.

        Adaptations:
            margin_top: additional margin required when considering
                        margin_bottom of the previous element

        Args:
            new: The new HtmlElement to be applied to the current context.

        Returns:
            The refined element with the context applied.
        """
        new.canvas = self.canvas
        if self.is_empty:
            new.list_bullet = self.list_bullet

        # inherit `display:none` attributes and ignore further refinements
        if self.display == Display.none:
            new.display = Display.none
            return new

        # no whitespace set => inherit
        new.whitespace = new.whitespace or self.whitespace

        # do not display whitespace only affixes in Whitespace.pre areas
        # if `limit_whitespace_affixes` is set.
        if (new.limit_whitespace_affixes
                and self.whitespace == WhiteSpace.pre):
            if new.prefix.isspace():
                new.prefix = ''
            if new.suffix.isspace():
                new.suffix = ''

        # total padding = current padding + the padding the refined element
        # introduces
        new.padding += self.padding

        # `Display.block` requires adjusting the `margin_before' and
        # `margin_after` attributes
        if new.display == Display.block:
            if self.tag == 'body':
                new.margin_before = 0
            else:
                new.margin_before = max(new.margin_before,
                                        self.margin_before)
            new.margin_after = max(new.margin_after,
                                   self.margin_after)
        return new

    WRITER = {
        Display.block: write_block_text,
        Display.inline: write_inline_text,
        Display.none: write_display_none
    }

    def __str__(self):
        return (
            '<{self.tag} prefix={self.prefix}, suffix={self.suffix}, '
            'display={self.display}, margin_before={self.margin_before}, '
            'margin_after={self.margin_after}, padding={self.padding}, '
            'list_bullet={self.list_bullet}, '
            'whitespace={self.whitespace}, align={self.align}, '
            'valign={self.valign}>'
        ).format(self=self)