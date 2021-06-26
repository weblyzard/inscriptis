r"""Parse HTML content and converts it into a text representation.

Inscriptis provides support for

 - nested HTML tables
 - basic Cascade Style Sheets
 - annotations

The following example provides the text representation of
`<https://www.fhgr.ch>`_.

.. code::

   import urllib.request
   from inscriptis.engine import get_text

   url = 'https://www.fhgr.ch'
   html = urllib.request.urlopen(url).read().decode('utf-8')

   text = get_text(html)

   print(text)

Use the method :meth:`~inscriptis.engine.get_annotated_text` to obtain text
and annotations. The method requires annotation rules as described in
annotations_.

.. code::

   import urllib.request
   from inscriptis.engine import get_annotated_text

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

__author__ = 'Albert Weichselbraun, Fabian Odoni'
__author_email__ = 'albert.weichselbraun@fhgr.ch, fabian.odoni@fhgr.ch'
__copyright__ = '2016-2021 Albert Weichselbraun, Fabian Odoni'
__license__ = 'Apache 2.0'
__version__ = '2.0rc1'
