import requests
from bs4 import BeautifulSoup
import json

url = 'https://en.wikipedia.org/wiki/'
#lines = open('wikis').read().split('\n')
flag = True 

while True:
    if flag:
        name = input('input page > ')
    
    flag = True

    res = requests.get(url + name)
    print(res)
    print('---')
    if res.status_code != 404:
        soup = BeautifulSoup(res.text, features="lxml")
        cats = soup.find(id="mw-normal-catlinks")
        if cats:
            li_tags = cats.find_all("li")
        newf = {"answer": name, "categories": []}
        potential = []

        i = 0
        for li in li_tags:
            potential.append(li.text)
            print(f'{i} {li.text}')
            i += 1
        
        accepted_cats = input('which cats (pick 5, in order) > ')
        if accepted_cats == 'q': 
            continue
        else:
            try:
                for i in [int(_) for _ in accepted_cats.split(' ')]:
                    newf['categories'].append(potential[i])
            except:
                name = accepted_cats
                flag = False
                continue

            output = open('potential_rounds.json', 'r')
            x = json.loads(output.read())
            x.append(newf)
            output.close()
            output = open('potential_rounds.json', 'w')
            output.write(json.dumps(x))
            output.close()

    else:
        print(f'{name} not found...')
        #best_match = process.extractOne(name, lines)
        #print(f'closest match: {best_match}')
