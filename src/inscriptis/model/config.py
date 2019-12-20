#!/usr/bin/env python
'''
Provides configuration objects for the Inscriptis HTML 2 text parser.
'''

from inscriptis.css_profiles import CSS_PROFILES

DEFAULT_CSS_PROFILE_NAME = 'relaxed'


class ParserConfig():
    '''
    The ParserConfig object encapsulates configuration options and custom CSS
    definitions used by inscriptis for translating HTML to text.
    '''
    def __init__(self, css=None, display_images=False,
                 deduplicate_captions=False, display_links=False,
                 display_anchors=False):
        '''
        Args:
            css: an optional custom CSS definition.
            display_images: whether to include image tiles/alt texts.
            deduplicate_captions: whether to deduplicate captions such as image
                titles (many newspaper include images and video previews with
                identifical titles).
            display_links: whether to display link targets
                           (e.g. `[Python](https://www.python.org)`).
            display_anchors: whether to display anchors (e.g. `[here](#here)`).

        '''

        self.css = css or CSS_PROFILES[DEFAULT_CSS_PROFILE_NAME]
        self.display_images = display_images
        self.deduplicate_captions = deduplicate_captions
        self.display_links = display_links
        self.display_anchors = display_anchors

    def parse_a(self):
        '''
        Returns:
            Whether we need to parse <a> tags.
        '''
        return self.display_links or self.display_anchors
