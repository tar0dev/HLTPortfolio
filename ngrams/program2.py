import pickle
from nltk import word_tokenize
from nltk.util import ngrams

def compute_prob(text, unigram_dict, bigram_dict, V) :
    # Calculate probabilities with Laplace Smoothing
    # V is the number of unique tokens, the vocabulary size
    unigrams_test = word_tokenize(text)
    bigrams_test = list(ngrams(unigrams_test, 2))
    p_laplace = 1
    for bigram in bigrams_test:
        n = bigram_dict[bigram] if bigram in bigram_dict else 0
        d = unigram_dict[bigram[0]] if bigram[0] in unigram_dict else 0
        p_laplace = p_laplace * ((n + 1) / (d + V))

    return p_laplace

def main():
    unigrams_dict_en = pickle.load(open('unigrams_dict_en.pkl', 'rb'))
    bigrams_dict_en = pickle.load(open('bigrams_dict_en.pkl', 'rb'))
    unigrams_dict_fr = pickle.load(open('unigrams_dict_fr.pkl', 'rb'))
    bigrams_dict_fr = pickle.load(open('bigrams_dict_fr.pkl', 'rb'))
    unigrams_dict_it = pickle.load(open('unigrams_dict_it.pkl', 'rb'))
    bigrams_dict_it = pickle.load(open('bigrams_dict_it.pkl', 'rb'))

    output = open('data/LangId.result', 'w')

    #open solution file
    sol = open('data/LangId.sol', 'r').readlines()
    lineNum = 1
    # counter for number of wrong predictions
    wrong = []

    # for each line in test file, calculate probability
    with open('data/LangId.test', 'r') as f:
        test = f.readlines()
        # Compute V for each dictionary

    V = len(unigrams_dict_en) + len(unigrams_dict_fr) + len(unigrams_dict_it)
    for line in test:

        line = line.strip()  # remove new line character
        en_prob = compute_prob(line, unigrams_dict_en, bigrams_dict_en, V)
        fr_prob = compute_prob(line, unigrams_dict_fr, bigrams_dict_fr, V)
        it_prob = compute_prob(line, unigrams_dict_it, bigrams_dict_it, V)
        highest_prob = max(en_prob, fr_prob, it_prob)
        if highest_prob == en_prob:
            language = "English"
        elif highest_prob == fr_prob:
            language = "French"
        elif highest_prob == it_prob:
            language = "Italian"

        output.write(str(lineNum) + ' ' + language + '\n')

        if str(str(lineNum) + ' ' + language + '\n') != sol[lineNum - 1]:
            wrong.append(str(lineNum))

        lineNum += 1

    #print accuracy
    accuracy = round(100 * (1 - (len(wrong) / lineNum)))
    output.write("Accuracy: " + str(accuracy) + "%\n")

    # print incorrect items
    if len(wrong) > 0:
        output.write("Line numbers of incorrect item below:\n")
        for item in wrong:
            output.write(item + "\n")
    output.close()

if __name__ == '__main__':
    main()
