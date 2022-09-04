import requests
from bs4 import BeautifulSoup
import re

inp_word = input('Print your word here:')
word = inp_word.capitalize()

def check(word):
    check_der = requests.get('https://der-artikel.de/der/' + word + '.html')
    if check_der:
        return "der"
    else:
        check_das = requests.get('https://der-artikel.de/das/' + word + '.html')
        if check_das:
            return "das"
        else:
            check_die = requests.get('https://der-artikel.de/die/' + word + '.html')
            if check_die:
                return "die"
            else:
                return None
if check(word) == None:
    print("Sorry, I don't know this word :(")
else:
    print(check(word) + " " + word)

def check_art():
    if check(word) == "der":
        return 'https://der-artikel.de/der/' + word + '.html'
    elif check(word) == "das":
        return 'https://der-artikel.de/das/' + word + '.html'
    elif check(word) == "die":
        return 'https://der-artikel.de/die/' + word + '.html'
    else:
        return None

url = check_art()
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")
element = soup.find("h3", class_="mb-5")
form_el = element.text.strip()

el = re.split('\W+', form_el)
trnsl = el[-1]
print("eng: " + trnsl)



