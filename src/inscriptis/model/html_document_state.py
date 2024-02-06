from inscriptis import ParserConfig
from inscriptis.model.canvas import Canvas


class HtmlDocumentState:
    """Represents the state of the parsed html document."""

    def __init__(self, config: ParserConfig = None):
        # instance variables
        self.canvas = Canvas()
        self.config = config
        self.css = config.css
        self.apply_attributes = config.attribute_handler.apply_attributes

        self.tags = [self.css["body"].set_canvas(self.canvas)]
        self.current_table = []
        self.li_counter = []
        self.last_caption = None

        # used if display_links is enabled
        self.link_target = ""
