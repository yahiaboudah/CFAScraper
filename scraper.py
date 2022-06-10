
import requests
from bs4 import BeautifulSoup
import json

cfa_link = "https://analystnotes.com/cfa-exam-2022.html"

# text_link = "https://analystnotes.com/cfa-study-notes-distinguish-between-unconditional-and-conditional-probabilities.html"

def get_cfa_link(link):
    return f'https://analystnotes.com/{link}'

def get_soup(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup


def get_text(page):

    soup = get_soup(page)
    text_card = soup.find('div', class_='card-block')

    if(text_card): cc = text_card.contents
    else: return 'No text'

    return [str(c) for c in cc]


def get_all_chunks(page):

    chunks = []

    soup = get_soup(page)
    table = soup.find('tbody')
    
    for tr in table.find_all('tr'):

        td = tr.find('td', class_='hidden-sm')
        chunk_a = td.find('a', href=True)
        
        if(chunk_a is None):
            chunks.append({
                'title': "Failed chunk",
                'text': "Wow such empty!"
            })

        chunk_title = chunk_a.contents[0]
        chunk_link = get_cfa_link(chunk_a['href'])

        descs = [str(x.contents) for x in tr.find_all('em')]
        
        print(f'Processing chunk: {chunk_title}')

        chunk_text = get_text(chunk_link)

        chunks.append({
            'title': chunk_title,
            'desc': descs,
            'text': chunk_text,
            'link': chunk_link 
        })

    return chunks

def get_all_readings(page):
    
    chunks = []
    readings = []

    soup = get_soup(page)
    table = soup.find('tbody')
    
    for tr in table.find_all('tr'):

        th = tr.find('th')
        reading_number = th.contents[0]
        reading_a = tr.find('td').find('a', href=True)
        reading_title = reading_a.contents[0]
        reading_link = get_cfa_link(reading_a['href'])

        print(f'Processing reading: {reading_number}')

        chunks = get_all_chunks(reading_link)

        readings.append({
            'number_title': reading_number,
            'title': reading_title,
            'chunks': chunks,
            'link': reading_link
        })

    return readings

def get_all_topics(page):

    root = {"topics": []}
    curr_topic = ""
    
    soup = get_soup(page)
    table = soup.find('tbody')
    
    for tr in table.find_all('tr'):
        
        th = tr.find('th')
        if(th): 
            curr_topic = th.contents[0]
            root['topics'].append({'name': curr_topic, 'sessions':[]})

        session_tag = tr.find('td', class_='hidden-sm').find('a', href=True)
        session_name = session_tag.contents[0]
        session_link = get_cfa_link(session_tag['href'])
        
        print(f'Processing {curr_topic}/{session_name}')
        
        curr_readings = get_all_readings(session_link)

        root['topics'] = list(map(lambda x:({
            'name': curr_topic,
            'sessions': x['sessions'] + [{
                "name": session_name,
                "readings": curr_readings,
                "link": session_link,
            }]
        } if x['name'] == curr_topic else x), root['topics']))

        with open('all_shit.json', 'w') as f:
            f.write(json.dumps(root, indent=4))

    return root


if __name__ == "__main__":
    
    ss = get_all_topics(cfa_link)
    ss = json.dumps(ss, indent=4)

    with open('dumb.json', 'w') as f:
        f.write(ss)