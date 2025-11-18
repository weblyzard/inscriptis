#!/usr/bin/env python3
"""Inscriptis command line client."""

import argparse
import sys
from json import dumps, load
from pathlib import Path

import requests

from inscriptis import get_annotated_text, get_text
from inscriptis.css_profiles import CSS_PROFILES
from inscriptis.metadata import __copyright__, __license__, __version__
from inscriptis.model.config import ParserConfig

DEFAULT_ENCODING = "utf8"
DEFAULT_TIMEOUT = 5  # default timeout in seconds


def get_postprocessor(name):
    """Return the postprocessor (if available) for the given name.

    Args:
        name: the name of the postprocessor

    Returns:
        The matching postprocessing function

    """
    pp_class = name.capitalize() + "Extractor"
    mod = __import__("inscriptis.annotation.output." + name, fromlist=[pp_class])
    return getattr(mod, pp_class)()


def parse_command_line() -> argparse.Namespace:
    """Parse the command line arguments.

    Returns:
        The parsed command line arguments.

    """
    parser = argparse.ArgumentParser(description="Convert the given HTML document to text.")
    parser.add_argument(
        "input",
        nargs="?",
        default=None,
        help="Html input either from a file or a URL (default:stdin).",
    )
    parser.add_argument("-o", "--output", type=str, help="Output file (default:stdout).")
    parser.add_argument(
        "-e",
        "--encoding",
        type=str,
        help="Input encoding to use (default:utf-8 for files; detected server encoding for Web URLs).",
    )
    parser.add_argument(
        "-i",
        "--display-image-captions",
        action="store_true",
        default=False,
        help="Display image captions (default:false).",
    )
    parser.add_argument(
        "-d",
        "--deduplicate-image-captions",
        action="store_true",
        default=False,
        help="Deduplicate image captions (default:false).",
    )
    parser.add_argument(
        "-l",
        "--display-link-targets",
        action="store_true",
        default=False,
        help="Display link targets (default:false).",
    )
    parser.add_argument(
        "-a",
        "--display-anchor-urls",
        action="store_true",
        default=False,
        help="Display anchor URLs (default:false).",
    )
    parser.add_argument(
        "-r",
        "--annotation-rules",
        default=None,
        help="Path to an optional JSON file containing rules for annotating the retrieved text.",
    )
    parser.add_argument(
        "-p",
        "--postprocessor",
        type=get_postprocessor,
        default=lambda x: x,
        help="Optional component for postprocessing the result (html, surface, xml). ",
    )
    parser.add_argument(
        "--indentation",
        default="extended",
        help="How to handle indentation (extended or strict; default: extended).",
    )
    parser.add_argument(
        "--table-cell-separator",
        default="  ",
        help="Separator to use between table cells (default: three spaces).",
    )
    parser.add_argument(
        "--timeout",
        default=DEFAULT_TIMEOUT,
        help=f"Request timeout in seconds (default: {DEFAULT_TIMEOUT}).",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="store_true",
        default=False,
        help="display version information",
    )

    # parse command line arguments
    args = parser.parse_args()
    if args.version:
        print(f"Inscript HTML to text conversion (based on the inscriptis library version {__version__})")
        print("Copyright (C)", __copyright__)
        print("\nInscript comes with ABSOLUTELY NO WARRANTY.")
        print(f"This is free software and you are welcome to redistribute it under the terms of the {__license__}.")
        sys.exit(0)
    return args


def get_html_content(url: str, timeout: int, encoding: str = "") -> str:
    """Return the HTML content to convert.

    Args:
        url: URL to the HTML content, or None if the content is obtained from stdin.
        encoding: used encoding.
        timeout: timeout in seconds for retrieving the URL.

    Returns:
        The html_content or None, if no content could be extracted.

    """
    if not url:
        return sys.stdin.read()
    if (p := Path(url)).is_file():
        with p.open(encoding=encoding or DEFAULT_ENCODING, errors="ignore") as f:
            return f.read()
    elif url.startswith(("http://", "https://")):
        req = requests.get(url, timeout=timeout)
        return req.content.decode(encoding or req.encoding)
    return ""


def cli() -> None:
    """Run the inscript command line client."""
    args = parse_command_line()
    if not (html_content := get_html_content(args.input, args.timeout, args.encoding)):
        print(f"ERROR: Cannot open input file '{args.input}'.")
        sys.exit(-1)

    if args.annotation_rules:
        try:
            with Path(args.annotation_rules).open() as f:
                annotation_rules = load(f)
        except OSError:
            print(f"ERROR: Cannot open annotation rule file '{args.annotation_rules}'.")
            sys.exit(-1)
    else:
        annotation_rules = None

    css_profile = CSS_PROFILES["relaxed"] if args.indentation == "extended" else CSS_PROFILES["strict"]
    config = ParserConfig(
        css=css_profile,
        display_images=args.display_image_captions,
        deduplicate_captions=args.deduplicate_image_captions,
        display_links=args.display_link_targets,
        display_anchors=args.display_anchor_urls,
        annotation_rules=annotation_rules,
        table_cell_separator=args.table_cell_separator,
    )
    if not annotation_rules:
        output = get_text(html_content, config)
    else:
        output = args.postprocessor(get_annotated_text(html_content, config))
        if hasattr(args.postprocessor, "verbatim") and not args.postprocessor.verbatim:
            output = dumps(output)

    if args.output:
        with Path(args.output).open("w", encoding=DEFAULT_ENCODING) as f:
            f.write(output)
    else:
        print(output)
