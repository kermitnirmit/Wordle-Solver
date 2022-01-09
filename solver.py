from collections import defaultdict
from random import sample
import re

words = open("words/words_alpha.txt").read().strip().splitlines()

gamelen = int(input("how many letters is the word? "))
words = list(filter(lambda x: len(x) == gamelen, words))
# print(len(words)) The real wordle list only has 2500 words and this has almost 16000

# sort by scrabble order // common letters higher up

def scrabble_score(word):
    valuemap = {
        'a': 1,
        'b': 3,
        'c': 3,
        'd': 2,
        'e': 1,
        'f': 4,
        'g': 2,
        'h': 4,
        'i': 1,
        'j': 8,
        'k': 5,
        'l': 1,
        'm': 3,
        'n': 1,
        'o': 1,
        'p': 3,
        'q': 10,
        'r': 1,
        's': 1,
        't': 1,
        'u': 1,
        'v': 4,
        'w': 4,
        'x': 8,
        'y': 4,
        'z': 10
    }
    score = 0
    
    for letter in word:
        score += valuemap[letter]
    return score

words.sort(key= lambda x: (scrabble_score(x), -1 * len(set(x))))

yellows = defaultdict(list)
greens = [""] * gamelen
wrongs = set()


def generate_green_str(greens):
    restr = ""
    for letter in greens:
        if letter == "":
            restr += "."
        else:
            restr += letter
    return restr


for i in range(6):
    print("number of words it could be: ", len(words))
    if len(words) > 15:
        print("some next guesses", words[:15])
        happy = False
        while not happy:
            answer = input("type y to see more guesses: ")
            if answer != "y":
                happy = True
            else:
                print("some next guesses", words[:15])
    else:
        print("some next guesses", words)

    user_guess = ""
    while len(user_guess) != gamelen:
        user_guess = input("Enter your guess: ")
    response = ""
    while len(response) != gamelen:
        response = input("Enter your result / 0 if not in there, 1 if yellow, 2 if green: ")
    if response == "2" * gamelen:
        break
    for index, (ug, r) in enumerate(zip(list(user_guess), list(response))):
        if r == "2":
            greens[index] = ug
        if r == "1":
            yellows[ug].append(index)
        if r == "0":
            wrongs.add(ug)
    for index, (ug, r) in enumerate(zip(list(user_guess), list(response))):
        if r == "0":  # this letter isn't there at all so remove those from the list --- NOT TRUE - if it's in wrongs and yellows then remove it from wrongs
            if ug in yellows.keys() or ug in greens:
                wrongs.remove(ug)
                yellows[ug].append(index)

    # Filtering stage
    greenStr = generate_green_str(greens)
    for letter in wrongs:
        words = list(filter(lambda x: letter not in x, words))
    r = re.compile(greenStr)
    words = list(filter(r.match, words))

    for letter, indexes in yellows.items():
        # letter is the letter, indexes is a list of indexes that the letter can't be in
        # so this eliminates all words that have that letter in that position
        for index in indexes:
            words = list(filter(lambda x: x[index] != letter, words))
        # but if a letter is a yellow, it has to be in the word to begin with
        words = list(filter(lambda x: letter in x, words))
