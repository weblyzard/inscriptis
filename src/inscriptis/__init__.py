"""
Inscriptis parses HTML content and converts it into a text representation.
Among others it provides support for

- nested HTML tables and
- basic Cascade Style Sheets.

Example::

   import urllib.request
   from inscriptis import get_text

   url = 'https://www.fhgr.ch'
   html = urllib.request.urlopen(url).read().decode('utf-8')

   text = get_text(html)

   print(text)

"""

__author__ = 'Albert Weichselbraun, Fabian Odoni'
__author_email__ = 'albert.weichselbraun@fhgr.ch, fabian.odoni@fhgr.ch'
__copyright__ = '2016-2021 Albert Weichselbraun, Fabian Odoni'
__license__ = 'Apache 2.0'
__version__ = '1.2'
