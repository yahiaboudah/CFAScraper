
from markdown_strings import *

import json
with open('all_shit.json', 'r') as f:
    ss = f.read()
    ss = json.loads(ss)

def topic_marker(rooter):
    res = ""
    for topic in rooter['topics']:
        res = res + header(topic['name'], 1) + "\n"
        
        for session in topic['sessions']:
            res = res + header(session['name'], 2) + "\n"
            for reading in session['readings']:
                res = res + header(reading['title'], 3) + "\n"
                for chunk in reading['chunks']:
                    res = res + header(chunk['title'], 4) + "\n"
                    res = res + ''.join(chunk['text']) + "\n"

    return res

rr = topic_marker(ss)

with open('mdresult.md', 'w', encoding='utf-8') as f:
    f.write(rr)