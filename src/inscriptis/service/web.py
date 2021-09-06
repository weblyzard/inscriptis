#!/usr/bin/env python3
# coding:utf-8
"""Inscriptis Web Service."""

from flask import request, Response, Flask

from inscriptis import get_text
from inscriptis.metadata import __version__
from inscriptis.css_profiles import RELAXED_CSS_PROFILE
from inscriptis.model.config import ParserConfig

app = Flask(__name__)
CONFIG = ParserConfig(css=RELAXED_CSS_PROFILE, display_images=True,
                      deduplicate_captions=True, display_links=False)


@app.route('/')
def index():
    """Print a short status message for the Web service's base URL."""
    return 'Inscriptis text to HTML Web service.'


@app.route('/get_text', methods=['POST'])
def get_text_call():
    """Return the text representation of the given HTML content."""
    content_type = request.headers['Content-type']
    if '; encoding=' in content_type:
        encoding = content_type.split('; encoding=')[1]
    else:
        encoding = 'UTF-8'
    html_content = request.data.decode(encoding, errors='ignore')
    text = get_text(html_content, CONFIG)
    return Response(text, mimetype='text/plain')


@app.route('/version', methods=['GET'])
def get_version_call():
    """Return the used inscriptis version."""
    return Response(__version__ + '\n', mimetype='text/plain')


if __name__ == '__main__':
    print('Starting Web service based on Inscriptis', __version__)
    app.run(threaded=True, host='127.0.0.1', port=5000)
