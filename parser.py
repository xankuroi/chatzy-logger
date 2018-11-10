# Parser for all those HTML files you generated
import os
import re
import json
from bs4 import BeautifulSoup as bs
from bs4.element import Comment as bscomment

# Regexes
bookmark_matcher = re.compile(r'<img class="X5047" onclick="X5047\(this\);return false;" onmouseover="X1584\(this\);" onmouseout="X1584\(\);" src="/elements/icon17/bookmark1\.png" title="Bookmark">')
color_matcher = re.compile(r'#?([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})')
time_matcher = re.compile(r'<a class="X5359">\w{3,5} ?\d{0,4}</a>')
name_matcher = re.compile(r'<b.*?color:(.*?)</b>')

def clear_matches(line):
    return name_matcher.sub('', time_matcher.sub('', line))

def get_timestamp(soup):
    return list(filter(lambda x: x.get('class') and ('X5359' in x.get('class')), soup.find_all('a')))[0].string

def clear_comments(bselements):
    filtered_list = list(filter(lambda x: type(x) != bscomment, bselements))
    return ''.join(list(map(lambda x: str(x), filtered_list)))

logs = os.listdir('logs/')
for i, log in enumerate(logs):
    with open(f'logs/{log}', 'r', encoding='utf-8') as l:
        with open(f'parsed_logs/{str(i).zfill(5)}.jsonl', 'w+', encoding='utf-8') as f:
            soup = bs(bookmark_matcher.sub('', l.read()), 'html.parser')
            for p in soup.find_all('p'):
                if p.get('class') and ('X7070' not in p.get('class')):
                    nametag = p.find('b')
                    if not nametag:
                        # These are likely class "b" messages. For now, ignore.
                        # Things like "so and so has entered the room"
                        # or other announcement type things
                        continue
                    f.write(
                        json.dumps(
                            {
                                't': p.get('class')[0],
                                'c': color_matcher.search(nametag.get('style'))[1],
                                'n': nametag.string,
                                'm': clear_matches(clear_comments(p.contents)),
                                'd': get_timestamp(p)
                            }, separators=(',', ':')
                        ) + '\n'
                    )
                    if 'c' in p.get('class'):
                        div = p.next_sibling
                        to_dump = { 't': 'div', 'm': clear_comments(div.contents) }
                        if p.get('style'):
                            to_dump = to_temp.update({'c': p.get('style')})
                        f.write(
                            json.dumps(to_dump, separators=(',', ':')) + '\n'
                        )
