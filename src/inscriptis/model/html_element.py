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
    - padding_inline: horizontal padding_inline before the tag's content.
    - whitespace: the :class:`~inscriptis.html_properties.Whitespace` handling
      strategy.
    - limit_whitespace_affixes: limit printing of whitespace affixes to
      elements with `normal` whitespace handling.
    """

    __slots__ = ('canvas', 'tag', 'prefix', 'suffix', 'display',
                 'margin_before', 'margin_after', 'padding_inline', 'list_bullet',
                 'whitespace', 'limit_whitespace_affixes', 'align', 'valign',
                 'is_empty', 'previous_margin_after')

    def __init__(self, tag='default', prefix='', suffix='', display=Display.inline,
                 margin_before=0, margin_after=0, padding_inline=0, list_bullet='',
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
        self.padding_inline = padding_inline
        self.list_bullet = list_bullet
        self.whitespace = whitespace
        self.limit_whitespace_affixes = limit_whitespace_affixes
        self.align = align
        self.valign = valign
        self.is_empty = True            # whether this is an empty element
        self.previous_margin_after = 0

    def write(self, text):
        """
        Writes the given HTML text.
        """
        if not text or self.display == Display.none:
            return

        self.canvas.write(self, ''.join(
            (self.prefix, text, self.suffix)))
        self.is_empty = False

    def write_tail(self, text):
        """
        Writes the tail text of an element.

        Args:
            text: the text to write
        """
        if not text:
            return
        self.write(text)

    def set_canvas(self, canvas):
        self.canvas = canvas
        return self

    def set_tag(self, tag):
        self.tag = tag
        return self

    def write_verbatim_text(self, tag, text):
        """
        Writes the given text verbatim to the canvas.
        Args:
            text: the text to write
        """
        if not text:
            return

        if tag.display == Display.block:
            self.canvas.open_block(tag)
        tag.whitespace = WhiteSpace.pre
        self.canvas.write(tag, text)

        if tag.display == Display.block:
            self.canvas.close_block(tag)

        #base_padding = ' ' * self.padding_inline
        #self.canvas.write(self, text.replace('\n', '\n' + base_padding))

    def close_block(self):
        """
        Closes a block in the canvas
        """
        self.canvas.close_block(self)

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

        if new.display == Display.block and self.display == Display.block:
            new.previous_margin_after = self.margin_after
        return new

    def __str__(self):
        return (
            '<{self.tag} prefix={self.prefix}, suffix={self.suffix}, '
            'display={self.display}, margin_before={self.margin_before}, '
            'margin_after={self.margin_after}, padding_inline={self.padding_inline}, '
            'list_bullet={self.list_bullet}, '
            'whitespace={self.whitespace}, align={self.align}, '
            'valign={self.valign}>'
        ).format(self=self)