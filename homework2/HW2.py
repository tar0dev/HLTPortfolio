import sys
import nltk
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from random import seed
from random import randint

def preprocess_text(raw_text):
    #not in stopword list
    # have length > 5

    # tokenize raw text into lowercase and only alpha
    stopwords_eng = stopwords.words('english')
    tokens = [t.lower() for t in word_tokenize(raw_text) if t.isalpha()]
    tokens_content = [t for t in tokens if t not in stopwords_eng and len(t) > 5]


    #lemmatize tokens
    wnl = WordNetLemmatizer()
    lemmatized = [wnl.lemmatize(t) for t in tokens_content]
    lemmas_unique = list(set(lemmatized))
    tags = nltk.pos_tag(lemmas_unique)
    for i in range(20):
        print(tags[i])



def main():
    if len(sys.argv) < 2:
        print('Please include the filename as a command line argument')
        print('Ex: python <filename>')
        quit()

    inputFile = sys.argv[1]

    with open(inputFile) as f:
        text_in = f.read()
        # tokenize text
        tokens = word_tokenize(text_in)
        set_tokens = set(tokens)
        # calculate lexical diversity
        lexical_div = len(set_tokens) / len(tokens)
        print(f'Lexical Diversity: ')
        print(lexical_div)

        preprocess_text(text_in)



if __name__ == '__main__':
    main()