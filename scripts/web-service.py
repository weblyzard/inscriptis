#!/usr/bin/env python3
# coding:utf-8
'''
Inscriptis Web Service
'''

from flask import request, Response, Flask
from inscriptis import get_text
from inscriptis.css_profiles import CSS_PROFILES
from inscriptis.model.config import ParserConfig

app = Flask(__name__)
config = ParserConfig(css=CSS_PROFILES['relaxed'], display_images=True,
                      deduplicate_captions=True, display_links=False)


@app.route("/")
def index():
    return "Hello"


@app.route("/get_text", methods=['POST'])
def get_text_call():
    content_type = request.headers['Content-type']
    if '; encoding=' in content_type:
        encoding = content_type.split('; encoding=')[1]
    else:
        encoding = 'UTF-8'
    html_content = request.data.decode(encoding, errors='ignore')
    text = get_text(html_content, config)
    return Response(text, mimetype='text/plain')


if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=5000)
