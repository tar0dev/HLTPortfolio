#CS 4395
# Jackie Le
# NetID: jll180004


import sys
import nltk
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
import random

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
    print("Unique Lemmas tagged: ", tags[:20])

    # list of lemmas that are only nouns
    nouns = []
    for word, pos in tags:
        if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS'):
            nouns.append(word)
    return tokens_content, nouns

def guess_game(words):
    # set a random word for the game
    game_word = random.choice(words)[0]
    # give user 5 points to start with
    user_points = 5
    hidden_word = ["_" for _ in game_word]
    guessed_letters = []
    print("---Starting Guessing Game!---\n")
    print(" ".join(hidden_word))
    print(game_word)
    while user_points > 0:
        # let user guess a letter
        letter = input("Guess a letter: ")

        # check if user wants to quit
        if letter == "!":
            print("Exiting program...")
            quit()
        # check if letter has already been guessed
        if letter in guessed_letters:
            print("You already guessed that letter, try again")
            continue
        guessed_letters.append(letter)
        # check if letter is in game word
        if letter in game_word:
            for i in range(len(game_word)):
                if game_word[i] == letter:
                    hidden_word[i] = letter
            print("Your guess was correct!")
            print(" ".join(hidden_word))
            # check if the word is complete
            if "_" not in hidden_word:
                print("You solved it and won with a score of:", user_points)
                return
        else:
            # if letter is not in game word, subtract a point
            user_points -= 1
            print("Sorry, guess again")
            print(" ".join(hidden_word))
            print("Your score is now:", user_points)
    # if user runs out of points, game is over
    print("You ran out of points, game over")
    print("The word was:", game_word)


def main():
    if len(sys.argv) < 2:
        print('Please include the filename as a command line argument')
        print('Ex: python <filename>')
        quit()

    inputFile = sys.argv[1]

    with open(inputFile) as f:
        text_in = f.read()
        # tokenize text
        tokens, nouns = preprocess_text(text_in)
        set_tokens = set(tokens)
        # calculate lexical diversity
        lexical_div = len(set_tokens) / len(tokens)
        print('Lexical Diversity: ', round(lexical_div, 2))


        #dictionary of nouns & sort dict by count
        nouns_dict = {t: tokens.count(t) for t in nouns}

        # print the 50 most common words and their counts. Save these words to a
        # list because they will be used in the guessing game.

        common_nouns = sorted(nouns_dict.items(), key=lambda x: x[1], reverse=True)
        # save list of 50 common words for guessing game
        list_words = []
        print("50 most common words:")
        for i in range(50):
            list_words.append(common_nouns[i])
            print(common_nouns[i])

        #call function for guessing game and pass in list
        guess_game(list_words)

if __name__ == '__main__':
    main()
