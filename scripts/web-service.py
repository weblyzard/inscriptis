#!/usr/bin/env python3
# coding:utf-8
"""
Inscriptis Web Service
"""

from flask import request, Response, Flask
from inscriptis import __version__
from inscriptis.engine import get_text
from inscriptis.css_profiles import RELAXED_CSS_PROFILE
from inscriptis.model.config import ParserConfig

app = Flask(__name__)
CONFIG = ParserConfig(css=RELAXED_CSS_PROFILE, display_images=True,
                      deduplicate_captions=True, display_links=False)


@app.route('/')
def index():
    return 'Hello'


@app.route('/get_text', methods=['POST'])
def get_text_call():
    """
    Returns:
        the text representation of the given HTML content.
    """
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
    """
    Returns:
        the used inscriptis version.
    """
    return Response(__version__ + '\n', mimetype='text/plain')


if __name__ == '__main__':
    print('Starting Web service based on Inscriptis', __version__)
    app.run(threaded=True, host='0.0.0.0', port=5000)
