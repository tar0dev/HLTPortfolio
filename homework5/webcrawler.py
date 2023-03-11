#Jackie Le
#CS 4395

from bs4 import BeautifulSoup
import requests
import pickle
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import re


def web_crawler(url):
    counter = 0
    # define soup object
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    # write urls to a file
    with open('urls.txt', 'w') as f:
        for link in soup.find_all('a'):
            link_str = str(link.get('href'))
            if 'basketball' in link_str or 'lakers' in link_str:
                if link_str.startswith('http') and 'google' not in link_str:
                    f.write(link_str + '\n')
                    counter += 1
            if counter >= 20:
                break


# scrape text from passed in relevant url and put into its own file
def scrape_text(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    # join all text from <p> elements
    text = ''
    for p in soup.select('p'):
        clean_text = p.get_text().replace("\t", " ").replace("\n", " ")
        clean_text = re.sub(r'\W+', ' ', clean_text)  # remove non-alphabetic characters
        text += clean_text + ' '
    with open('link.txt', "w") as file:
        file.write(text)


def extract_terms():
    freqDict = {}
    with open('link.txt', "r") as f:
        text = f.read()
        tokens = word_tokenize(text)
        tokens = [t.lower() for t in tokens]
        tokens = [t for t in tokens if t.isalpha() and t not in stopwords.words('english')]
        token_set = set(tokens)

        for t in token_set:
            if t in freqDict:
                freqDict[t] = freqDict[t] + tokens.count(t)
            else:
                freqDict[t] = tokens.count(t)
    sorted_counts = sorted(freqDict.items(), key=lambda x: x[1], reverse=True)
    print("Most common words in all pages:")
    for i in range(min(25, len(sorted_counts))):
        print(sorted_counts[i])

if __name__ == '__main__':

    starter_url = 'https://en.wikipedia.org/wiki/Kobe_Bryant'

    r = requests.get(starter_url)

    data = r.text
    soup = BeautifulSoup(data, 'html.parser')

    #find relevant links to starter url
    web_crawler(starter_url)
    scrape_text(starter_url)
    extract_terms()