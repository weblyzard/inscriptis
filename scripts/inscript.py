#!/usr/bin/env python3
# coding:utf-8
'''
Converts HTML to Text

Guiding principles:

 a. break lines only if we encounter a block element
 b. paddings:
'''

__author__ = "Fabian Odoni, Albert Weichselbraun, Samuel Abels"
__copyright__ = "Copyright 2015, HTW Chur"
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Fabian Odoni"
__email__ = "fabian.odoni@htwchur.ch"
__status__ = "Prototype"

from urllib.request import urlopen
import argparse

from inscriptis import get_text


def get_args():
    """ Parses the arguments if script is run directly via console """
    parser = argparse.ArgumentParser(description='Converts HTML from file or url to a clean text version')
    parser.add_argument('input', help='Html input either from a file or an url')
    parser.add_argument('-o', '--output', type=str, help='Output file (default:stdout).')
    parser.add_argument('-e', '--encoding', type=str, help='Content encoding for files (default:utf-8)', default='utf-8')
    parser.add_argument('-i', '--image-captions', action='store_true', default=False, help='Display image captions (default:false).')
    parser.add_argument('-d', '--deduplicate-image-captions', action='store_true', default=False, help='Deduplicate image captions (default:false).')
    args = parser.parse_args()

    return args


if __name__ == "__main__":
    args = get_args()

    if args.input.startswith("http://") or args.input.startswith("https://"):
        html_content = urlopen(args.input)
    else:
        with open(args.input, encoding=args.encoding) as f:
            html_content = f.read()

    text = get_text(html_content,
                    display_images=args.image_captions,
                    deduplicate_captions=args.deduplicate_image_captions)
    if args.output:
        with open(args.output, 'w') as open_file:
            open_file.write(text)
    else:
        print(text)

