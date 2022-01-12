from collections import defaultdict, Counter
import re

import sys

words = open("words/words_alpha.txt").read().strip().splitlines()
gamelen = int(sys.argv[1])
words = list(filter(lambda x: len(x) == gamelen, words))

saved_orig = words

# print(len(words)) The real wordle list only has 2500 words and this has almost 16000

yellows = defaultdict(list)
greens = [""] * gamelen
wrongs = set()
doubles = set()

greensfilled = 0

def getWordsWithLetters(wordlist, letters):
    nlist = []
    for word in wordlist:
        if len(letters & set(word)) > 0:
            nlist.append(word)

    def score(w):
        return len(set(w) & letters)
    nlist.sort(key= lambda x: score(x), reverse=True)
    return nlist

def generate_green_str(greens):
    restr = ""
    for letter in greens:
        if letter == "":
            restr += "."
        else:
            restr += letter
    return restr

def find_most_common_at_index(i, words):
    a = defaultdict(int)
    for word in words:
        a[word[i]] += 1
    return a

def commonscore(commons, word):
    score = 0
    for index, letter in enumerate(word):
        score += commons[index][letter]
    return score

for i in range(6):
    most_commons = [find_most_common_at_index(index, words) for index in range(gamelen)]
    words.sort(key = lambda x: commonscore(most_commons, x), reverse=True)
    emptyspots = []
    if greensfilled >= gamelen - 2:
        for index, val in enumerate(greens):
            if val == "":
                emptyspots.append(index)
        remainingLetters = set()
        for spot in emptyspots:
            for x in words:
                remainingLetters.add(x[spot])
        print("possible missing letters", remainingLetters)
        qwords = getWordsWithLetters(saved_orig, remainingLetters)
        print("words that have the potential missing letters", qwords[:15])

    print("number of words it could be: ", len(words))
    print("some next guesses", words[:15])

    user_guess = ""
    while len(user_guess) != gamelen:
        user_guess = input("Enter your guess: ")
    response = ""
    while len(response) != gamelen:
        response = input("Enter your result / 0 if not in there, 1 if yellow, 2 if green: ")
    if response == "2" * gamelen:
        break
    greensthistime = []
    for index, (ug, r) in enumerate(zip(list(user_guess), list(response))):
        if r == "2":
            if greens[index] == "":
                greensfilled += 1
            greens[index] = ug
            greensthistime.append(ug)
        if r == "1":
            yellows[ug].append(index)
        if r == "0":
            wrongs.add(ug)
    for index, (ug, r) in enumerate(zip(list(user_guess), list(response))):
        if r == "0":  # if it's in wrongs and yellows then remove it from wrongs
            if (ug in yellows.keys() or ug in greens) and ug in wrongs:
                wrongs.remove(ug)
                yellows[ug].append(index)
        if r == "1":
            if ug in greensthistime:
                doubles.add(ug)

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
        if letter in doubles:
            words = list(filter(lambda x: Counter(x)[letter] >= 2, words))
        else:
            words = list(filter(lambda x: letter in x, words))
