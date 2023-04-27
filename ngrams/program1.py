# Jackie Le
# CS4395


# Import required libraries
from nltk import word_tokenize
from nltk.util import ngrams
import pickle


# Function to read the input file and generate n-grams
def generate_ngrams(filename):
    text_in = open(filename).read()
    content = text_in.replace('\n', '')
    # Generate n-grams
    unigrams = word_tokenize(content)
    bigrams = list(ngrams(unigrams, 2))

    unigram_dict = {t: unigrams.count(t) for t in set(unigrams)}
    bigram_dict = {b: bigrams.count(b) for b in set(bigrams)}

    return unigram_dict, bigram_dict

if __name__ == '__main__':
    # Check if filename and n are provided as arguments

    eng_file = 'data/LangId.train.English'
    fr_file = 'data/LangId.train.French'
    it_file = 'data/LangId.train.Italian'
    unigrams_dict_en, bigrams_dict_en = generate_ngrams(eng_file)
    unigrams_dict_fr, bigrams_dict_fr = generate_ngrams(fr_file)
    unigrams_dict_it, bigrams_dict_it = generate_ngrams(it_file)

    #pickle files
    with open('unigrams_dict_en.pkl', 'wb') as f:
        pickle.dump(unigrams_dict_en, f)
    with open('bigrams_dict_en.pkl', 'wb') as f:
        pickle.dump(bigrams_dict_en, f)
    with open('unigrams_dict_fr.pkl', 'wb') as f:
        pickle.dump(unigrams_dict_fr, f)
    with open('bigrams_dict_fr.pkl', 'wb') as f:
        pickle.dump(bigrams_dict_fr, f)
    with open('unigrams_dict_it.pkl', 'wb') as f:
        pickle.dump(unigrams_dict_it, f)
    with open('bigrams_dict_it.pkl', 'wb') as f:
        pickle.dump(bigrams_dict_it, f)