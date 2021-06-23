"""Utils for calling inscriptis."""

import re
import lxml.html

from typing import Dict, Optional

from inscriptis.model.config import ParserConfig
from inscriptis.html_engine import Inscriptis

RE_STRIP_XML_DECLARATION = re.compile(r'^<\?xml [^>]+?\?>')


def _get_html_tree(html_content: str) -> Optional[lxml.html.HtmlElement]:
    """Obtain the HTML parse tree for the given HTML content.

    Args:
        html_content: The content to parse.

    Returns:
        The corresponding HTML parse tree.
    """
    html_content = html_content.strip()
    if not html_content:
        return None

    # strip XML declaration, if necessary
    if html_content.startswith('<?xml '):
        html_content = RE_STRIP_XML_DECLARATION.sub('', html_content, count=1)

    return lxml.html.fromstring(html_content)


def get_text(html_content: str, config: ParserConfig = None) -> str:
    """Provide a text representation of the given HTML content.

    Args:
      html_content (str): The HTML content to convert.
      config: An optional ParserConfig object.

    Returns:
      The text representation of the HTML content.
    """
    html_tree = _get_html_tree(html_content)
    return Inscriptis(html_tree, config).get_text() if html_tree is not None \
        else ''


def get_annotated_text(html_content: str,
                       config: ParserConfig = None) -> Dict[str, str]:
    """Return a dictionary of the extracted text and annotations.

    Notes:
        - the text is stored under the key 'text'.
        - annotations are provided under the key 'label' in the JSONL format.

    Examples:
        {"text": "EU rejects German call to boycott British lamb.", "
         label": [ [0, 2, "strong"], ... ]}
        {"text": "Peter Blackburn",
         "label": [ [0, 15, "heading"] ]}

    Returns:
        A dictionary of text (key: 'text') and annotations (key: 'label')
    """
    html_tree = _get_html_tree(html_content)
    if html_tree is None:
        return {}

    inscriptis = Inscriptis(html_tree, config)
    labels = [(a.start, a.end, a.metadata)
              for a in inscriptis.get_annotations()]
    return {'text': inscriptis.get_text(),
            'label': labels}
