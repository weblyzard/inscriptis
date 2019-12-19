#!/usr/bin/env python3
# coding:utf-8
'''
Inscriptis command line client.
'''

import requests
import argparse
import sys
from os.path import isfile

from inscriptis import get_text
from inscriptis.css_profiles import CSS_PROFILES


def get_parser():
    """ Parses the arguments if script is run directly via console """
    parser = argparse.ArgumentParser(description='Converts HTML from file or url to a clean text version')
    parser.add_argument('input', nargs='?', default=None, help='Html input either from a file or an url (default:stdin)')
    parser.add_argument('-o', '--output', type=str, help='Output file (default:stdout).')
    parser.add_argument('-e', '--encoding', type=str, help='Content encoding for files (default:utf-8)', default='utf-8')
    parser.add_argument('-i', '--display-image-captions', action='store_true', default=False, help='Display image captions (default:false).')
    parser.add_argument('-l', '--display-link-targets', action='store_true', default=False, help='Display link targets (default:false).')
    parser.add_argument('-d', '--deduplicate-image-captions', action='store_true', default=False, help='Deduplicate image captions (default:false).')
    parser.add_argument('--indentation', default='extended', help='How to handle indentation (extended or standard; default: standard).')
    return parser


if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()

    if not args.input:
        html_content = sys.stdin.read()
    elif isfile(args.input):
        with open(args.input, encoding=args.encoding, errors='ignore') as f:
            html_content = f.read()
    elif args.input.startswith("http://") or args.input.startswith("https://"):
        html_content = requests.get(args.input).text
    else:
        print("ERROR: Cannot open input file '{}'.\n".format(args.input))
        parser.print_help()
        sys.exit(-1)

    css_profile = CSS_PROFILES['relaxed'] if args.indentation == 'extended' \
        else CSS_PROFILES['strict']
    text = get_text(html_content,
                    display_images=args.display_image_captions,
                    deduplicate_captions=args.deduplicate_image_captions,
                    display_links=args.display_link_targets,
                    css_profile=css_profile)
    if args.output:
        with open(args.output, 'w') as open_file:
            open_file.write(text)
    else:
        print(text)
