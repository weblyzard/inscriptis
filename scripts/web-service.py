#!/usr/bin/env python3
# coding:utf-8
'''
Inscriptis Web Service
'''

from flask import request, Response, Flask
from inscriptis import get_text

app = Flask(__name__)

@app.route("/get_text", methods=['POST'])
def get_text_call():
    content_type = request.headers['Content-type']
    if '; encoding=' in content_type:
        encoding = content_type.split('; encoding=')[1]
    else:
        encoding = 'UTF-8'
    html_content = request.data.decode(encoding, errors='ignore')
    text = get_text(html_content,
                    display_images=True,
                    deduplicate_captions=True,
                    display_links=False)
    return Response(text, mimetype='text/plain')
