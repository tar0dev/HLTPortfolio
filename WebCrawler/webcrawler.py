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
            if 'ethereum' in link_str or 'blockchain' in link_str:
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
    with open(f'link.txt', "w") as file:
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
    #print("Most common words in all pages:")
    #for i in range(min(25, len(sorted_counts))):
      #  print(sorted_counts[i])

def buildKnowledgeBase():
    knowledgeBase = {
        'ethereum': 'Ethereum is a decentralized open source blockchain with smart contract functionality',
        'ether': 'Ether is the native currency that Ethereum uses',
        'blockchain' : 'A blockchain is a distributed ledger with growing lists of records (blocks) that are securely linked together via cryptographic hashes.' ,
        'stake:': 'On 15 September 2022, Ethereum transitioned its consensus mechanism from proof-of-work (PoW) to proof-of-stake (PoS) in an upgrade process known as "the Merge".',
        'decetralized': 'Decentralized finance (DeFi) offers traditional financial instruments in a decentralized architecture, outside of companies and governments control, such as money market funds which let users earn interest.',
        'contract': 'A smart contract is a computer program or a transaction protocol that is intended to automatically execute',
        'buterin': 'Ethereum was conceived in 2013 by programmer Vitalik Buterin.',
        'block': ' Each block contains a cryptographic hash identifying the series of blocks that must precede it if the block is to be considered valid.',
        'cryptocurrency':'Ether (ETH) is the cryptocurrency generated in accordance with the Ethereum protocol as a reward to validators in a proof-of-stake system for adding blocks to the blockchain.',
        'gas': 'Gas is a unit of account within the EVM used in the calculation of the transaction fee, which is the amount of ETH a transactions sender must pay to the network to have the transaction included in the blockchain.'
    }
    pickle.dump(knowledgeBase, open('knowledgeBase.p', 'wb'))


if __name__ == '__main__':

    starter_url = 'https://en.wikipedia.org/wiki/Ethereum'

    r = requests.get(starter_url)

    data = r.text
    soup = BeautifulSoup(data, 'html.parser')

    #find relevant links to starter url
    web_crawler(starter_url)

    with open('urls.txt', "r") as f:
        sentences = f.read().splitlines()
    for sent in sentences:
        scrape_text(sent)

    extract_terms()
    buildKnowledgeBase()