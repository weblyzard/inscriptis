#!/usr/bin/env python3
# coding:utf-8
"""Inscriptis command line client."""

import argparse
import sys
from json import load, dumps
from pathlib import Path

import requests

from inscriptis import get_text, get_annotated_text
from inscriptis.metadata import __version__, __copyright__, __license__
from inscriptis.css_profiles import CSS_PROFILES
from inscriptis.model.config import ParserConfig

DEFAULT_ENCODING = 'utf8'


def get_postprocessor(name):
    """Return the postprocessor (if available) for the given name.

    Args:
        name: the name of the postprocessor

    Returns:
        The matching postprocessing function
    """
    pp_class = name.capitalize() + 'Extractor'
    mod = __import__('inscriptis.annotation.output.' + name,
                     fromlist=[pp_class])
    return getattr(mod, pp_class)()


def get_parser():
    """Parse the arguments if script is run via console."""
    parser = argparse.ArgumentParser(
        description='Convert the given HTML document to text.')
    parser.add_argument('input', nargs='?', default=None,
                        help='Html input either from a file or a URL '
                             '(default:stdin).')
    parser.add_argument('-o', '--output', type=str,
                        help='Output file (default:stdout).')
    parser.add_argument('-e', '--encoding', type=str,
                        help='Input encoding to use (default:utf-8 for '
                             'files; detected server encoding for Web URLs).')
    parser.add_argument('-i', '--display-image-captions',
                        action='store_true', default=False,
                        help='Display image captions (default:false).')
    parser.add_argument('-d', '--deduplicate-image-captions',
                        action='store_true', default=False,
                        help='Deduplicate image captions (default:false).')
    parser.add_argument('-l', '--display-link-targets',
                        action='store_true', default=False,
                        help='Display link targets (default:false).')
    parser.add_argument('-a', '--display-anchor-urls',
                        action='store_true', default=False,
                        help='Deduplicate image captions (default:false).')
    parser.add_argument('-r', '--annotation-rules', default=None,
                        help='Path to an optional JSON file containing rules '
                             'for annotating the retrieved text.')
    parser.add_argument('-p', '--postprocessor', type=get_postprocessor,
                        default=lambda x: x,
                        help='Optional component for postprocessing the '
                             'result (html, surface, xml). ')
    parser.add_argument('--indentation', default='extended',
                        help='How to handle indentation (extended or strict;'
                             ' default: extended).')
    parser.add_argument('-v', '--version',
                        action='store_true', default=False,
                        help='display version information')
    return parser


if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()

    if args.version:
        print('Inscript HTML to text conversion (based on the inscriptis '
              'library version {0})'.format(__version__))
        print('Copyright (C)', __copyright__)
        print('\nInscript comes with ABSOLUTELY NO WARRANTY.')
        print('This is free software and you are welcome to redistribute it '
              'under the terms of the {0}.'.format(__license__))
        sys.exit(0)

    if not args.input:
        html_content = sys.stdin.read()
    elif Path(args.input).is_file():
        with Path(args.input).open(encoding=args.encoding or DEFAULT_ENCODING,
                                   errors='ignore') as f:
            html_content = f.read()
    elif args.input.startswith('http://') or args.input.startswith('https://'):
        req = requests.get(args.input)
        html_content = req.content.decode(args.encoding or req.encoding)
    else:
        print("ERROR: Cannot open input file '{0}'.\n".format(args.input))
        parser.print_help()
        sys.exit(-1)

    if args.annotation_rules:
        try:
            with Path(args.annotation_rules).open() as f:
                annotation_rules = load(f)
        except IOError:
            print("ERROR: Cannot open annotation rule file '{0}'.".format(
                args.annotation_rules
            ))
            sys.exit(-1)
    else:
        annotation_rules = None

    css_profile = CSS_PROFILES['relaxed'] if args.indentation == 'extended' \
        else CSS_PROFILES['strict']
    config = ParserConfig(css=css_profile,
                          display_images=args.display_image_captions,
                          deduplicate_captions=args.deduplicate_image_captions,
                          display_links=args.display_link_targets,
                          display_anchors=args.display_anchor_urls,
                          annotation_rules=annotation_rules)
    if not annotation_rules:
        output = get_text(html_content, config)
    else:
        output = args.postprocessor(
            get_annotated_text(html_content, config))
        if hasattr(args.postprocessor, 'verbatim') \
           and not args.postprocessor.verbatim:
            output = dumps(output)

    if args.output:
        with Path(args.output).open('w', encoding=DEFAULT_ENCODING) as f:
            f.write(output)
    else:
        print(output)
