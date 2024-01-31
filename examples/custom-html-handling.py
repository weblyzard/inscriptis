#!/usr/bin/env python3

from inscriptis import Inscriptis

inscriptis = Inscriptis(html, config)



inscriptis.start_tag_handler_dict['a'] = my_handle_start_a
inscriptis.end_tag_handler_dict['a'] = my_handle_end_a
text = inscriptis.get_text()
