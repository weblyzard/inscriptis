==================================================================================
inscriptis -- HTML to text conversion library, command line client and Web service
==================================================================================

.. image:: https://img.shields.io/pypi/pyversions/inscriptis   
   :target: https://badge.fury.io/py/inscriptis
   :alt: PyPI - Python Version

.. image:: https://badge.fury.io/py/inscriptis.svg
   :target: https://badge.fury.io/py/inscriptis
   :alt: PyPI version

.. image:: https://codecov.io/gh/weblyzard/inscriptis/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/weblyzard/inscriptis/
   :alt: Coverage

.. image:: https://www.travis-ci.org/weblyzard/inscriptis.png?branch=master
   :target: https://www.travis-ci.org/weblyzard/inscriptis
   :alt: Build status

.. image:: https://readthedocs.org/projects/inscriptis/badge/?version=latest
   :target: https://inscriptis.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

A python based HTML to text conversion library, command line client and Web service with support for **nested tables** and a **subset of CSS**.
Please take a look at the `Rendering <https://github.com/weblyzard/inscriptis/blob/master/RENDERING.md>`_ document for a demonstration of inscriptis' conversion quality.

Documentation
=============

The full documentation is built automatically and published on `Read the Docs <https://inscriptis.readthedocs.org/en/latest/>`_.

Table of Contents
=================

1. `Installation`_
2. `Python library`_
3. `Standalone command line client`_
4. `Web service`_
5. `Fine tuning`_
6. `Changelog`_


Installation
============

At the command line::

    $ pip install inscriptis

Or, if you don't have pip installed::

    $ easy_install inscriptis

If you want to install from the latest sources, you can do::

    $ git clone https://github.com/weblyzard/inscriptis.git
    $ cd inscriptis
    $ python setup.py install


Python library
==============

Embedding inscriptis into your code is easy, as outlined below::
   
   import urllib.request
   from inscriptis import get_text
   
   url = "https://www.informationscience.ch"
   html = urllib.request.urlopen(url).read().decode('utf-8')
   
   text = get_text(html)
   print(text)


Standalone command line client
==============================
The command line client converts HTML files or text retrieved from Web pages to the
corresponding text representation.


Command line parameters
-----------------------
The inscript.py command line client supports the following parameters::

   usage: inscript.py [-h] [-o OUTPUT] [-e ENCODING] [-i] [-d] [-l] [-a]
                      [--indentation INDENTATION] [-v]
                      [input]
   
   Converts HTML from file or url to a clean text version
   
   positional arguments:
     input                 Html input either from a file or an url
                           (default:stdin)
   
   optional arguments:
     -h, --help            show this help message and exit
     -o OUTPUT, --output OUTPUT
                           Output file (default:stdout).
     -e ENCODING, --encoding ENCODING
                           Content encoding for reading and writing files
                           (default:utf-8)
     -i, --display-image-captions
                           Display image captions (default:false).
     -d, --deduplicate-image-captions
                           Deduplicate image captions (default:false).
     -l, --display-link-targets
                           Display link targets (default:false).
     -a, --display-anchor-urls
                           Deduplicate image captions (default:false).
     --indentation INDENTATION
                           How to handle indentation (extended or strict;
                           default: extended).
     -v, --version         display version information
   

Examples
--------

convert the given page to text and output the result to the screen::

  $ inscript.py https://www.fhgr.ch
   
convert the file to text and save the output to output.txt::

  $ inscript.py fhgr.html -o fhgr.txt
   
convert text provided via stdin and save the output to output.txt::

  $ echo '<body><p>Make it so!</p>></body>' | inscript.py -o output.txt 



Web Service
===========

The Flask Web Service translates HTML pages to the corresponding plain text. 

Additional Requirements
-----------------------

* python3-flask

Startup
-------
Start the inscriptis Web service with the following command::

  $ export FLASK_APP="web-service.py"
  $ python3 -m flask run

Usage
-----

The Web services receives the HTML file in the request body and returns the corresponding text. The file's encoding needs to be specified 
in the `Content-Type` header (`UTF-8` in the example below)::

  $ curl -X POST  -H "Content-Type: text/html; encoding=UTF8" --data-binary @test.html  http://localhost:5000/get_text

The service also supports a version call::

  $ curl http://localhost:5000/version


Fine tuning
===========

The following options are available for fine tuning inscriptis' HTML rendering:

1. **More rigorous indentation:** call `inscriptis.get_text()` with the parameter `indentation='extended'` to also use indentation for tags such as `<div>` and `<span>` that do not provide indentation in their standard definition. This strategy is the default in `inscript.py` and many other tools such as lynx. If you do not want extended indentation you can use the parameter `indentation='standard'` instead.

2. **Overwriting the default CSS definition:** inscriptis uses CSS definitions that are maintained in `inscriptis.css.CSS` for rendering HTML tags. You can override these definitions (and therefore change the rendering) as outlined below::

      from lxml.html import fromstring
      from inscriptis.css_profiles import CSS_PROFILES, HtmlElement
      from inscriptis.html_properties import Display
      from inscriptis.model.config import ParserConfig
      
      # create a custom CSS based on the default style sheet and change the rendering of `div` and `span` elements
      css = CSS_PROFILES['strict'].copy()
      css['div'] = HtmlElement('div', display=Display.block, padding=2)
      css['span'] = HtmlElement('span', prefix=' ', suffix=' ')
      
      html_tree = fromstring(html)
      # create a parser using a custom css
      config = ParserConfig(css=css)
      parser = Inscriptis(html_tree, config)
      text = parser.get_text()
   

Changelog
=========

A full list of changes can be found in the `release notes <https://github.com/weblyzard/inscriptis/releases>`_.
