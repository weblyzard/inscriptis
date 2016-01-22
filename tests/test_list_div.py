#!/usr/bin/env python

''' ensures that two successive <a>text</a> contain
    a space between each other, if there is a linebreak
    or space between the tags.
'''

from inscriptis import get_text

def test_divs():
    html = u'<body>Thomas<div>Anton</div>Maria</body>'
    assert get_text(html) == 'Thomas\nAnton\nMaria'

    html = u'<body>Thomas<div>Anna <b>läuft</b> weit weg.</div>'
    assert get_text(html) == 'Thomas\nAnna läuft weit weg.'

    html = u'<body>Thomas <ul><li><div>Anton</div>Maria</ul></body>'
    assert get_text(html) == 'Thomas\n  * Anton\n    Maria'

    html = u'<body>Thomas <ul><li>  <div>Anton</div>Maria</ul></body>'
    assert get_text(html) == 'Thomas\n  * Anton\n    Maria'

    html = u'<body>Thomas <ul><li> a  <div>Anton</div>Maria</ul></body>'
    assert get_text(html) == 'Thomas\n  * a\n    Anton\n    Maria'


