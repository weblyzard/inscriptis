r"""Parse HTML content and converts it into a text representation.

Inscriptis provides support for

 - nested HTML tables
 - basic Cascade Style Sheets
 - annotations

The following example provides the text representation of
`<https://www.fhgr.ch>`_.

.. code::

   import urllib.request
   from inscriptis import get_text

   url = 'https://www.fhgr.ch'
   html = urllib.request.urlopen(url).read().decode('utf-8')

   text = get_text(html)

   print(text)

Use the method :meth:`~inscriptis.get_annotated_text` to obtain text and
annotations. The method requires annotation rules as described in annotations_.

.. code::

   import urllib.request
   from inscriptis import get_annotated_text

   url = "https://www.fhgr.ch"
   html = urllib.request.urlopen(url).read().decode('utf-8')

   # annotation rules specify the HTML elements and attributes to annotate.
   rules = {'h1': ['heading'],
            'h2': ['heading'],
            '#class=FactBox': ['fact-box'],
            'i': ['emphasis']}

  output = get_annotated_text(html, ParserConfig(annotation_rules=rules)
  print("Text:", output['text'])
  print("Annotations:", output['label'])

The method returns a dictionary with two keys:

 1. `text` which contains the page's plain text and
 2. `label` with the annotations in JSONL format that is used by annotators
     such as `doccano <https://doccano.herokuapp.com/>`_.

Annotations in the `label` field are returned as a list of triples with
 `start index`, `end index` and `label` as indicated below:

.. code-block:: json

   {"text": "Chur\n\nChur is the capital and largest town of the Swiss canton
             of the Grisons and lies in the Grisonian Rhine Valley.",
    "label": [[0, 4, "heading"], [6, 10, "emphasis"]]}

"""

import re
from typing import Dict, Optional, Any
from inscriptis.model.config import ParserConfig

from lxml.etree import ParserError
from lxml.html import fromstring, HtmlElement

from inscriptis.html_engine import Inscriptis

RE_STRIP_XML_DECLARATION = re.compile(r"^<\?xml [^>]+?\?>")


def _get_html_tree(html_content: str) -> Optional[HtmlElement]:
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
    if html_content.startswith("<?xml "):
        html_content = RE_STRIP_XML_DECLARATION.sub("", html_content, count=1)

    try:
        return fromstring(html_content)
    except ParserError:
        return fromstring("<pre>" + html_content + "</pre>")


def get_text(html_content: str, config: ParserConfig = None) -> str:
    """Provide a text representation of the given HTML content.

    Args:
      html_content (str): The HTML content to convert.
      config: An optional ParserConfig object.

    Returns:
      The text representation of the HTML content.
    """
    html_tree = _get_html_tree(html_content)
    return Inscriptis(html_tree, config).get_text() if html_tree is not None else ""


def get_annotated_text(
    html_content: str, config: ParserConfig = None
) -> Dict[str, Any]:
    """Return a dictionary of the extracted text and annotations.

    Notes:
        - the text is stored under the key 'text'.
        - annotations are provided under the key 'label' which contains a
          list of :class:`Annotation`s.

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
    text = inscriptis.get_text()
    labels = [(a.start, a.end, a.metadata) for a in inscriptis.get_annotations()]
    return {"text": text, "label": labels}
