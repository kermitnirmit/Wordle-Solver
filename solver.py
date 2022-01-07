from collections import defaultdict
from random import sample
import re

words = open("words/words_alpha.txt").read().strip().splitlines()

gamelen = int(input("how many letters is the word? "))

words = list(filter(lambda x: len(x) == gamelen, words))
# print(len(words)) The real wordle list only has 2500 words and this has almost 16000
yellows = defaultdict(list)
greens = [""] * gamelen
wrongs = set()

def generateGreenStr(greens):
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
        print("some next guesses", sample(words, 15))
        happy = False
        while not happy:
            answer = input("type y to see more guesses: ")
            if answer != "y":
                happy = True
            else:
                print("some next guesses", sample(words, 15))
    else:
        print("some next guesses", words)


    user_guess = ""
    while len(user_guess) != gamelen:
        user_guess = input("Enter your guess: ")
    response = ""
    while len(response) != gamelen:
        response = input("Enter your result / 0 if not in there, 1 if yellow, 2 if green: ")
    if response == "2"*gamelen:
        break
    for index, (ug, r) in enumerate(zip(list(user_guess), list(response))):
        if r == "2":
            greens[index] = ug
        if r == "1":
            yellows[ug].append(index)
        if r == "0": # this letter isn't there at all so remove those from the list --- NOT TRUE - if it's in wrongs and yellows then remove it from wrongs
            wrongs.add(ug)
    for index, (ug, r) in enumerate(zip(list(user_guess), list(response))):
        if r == "0": # this letter isn't there at all so remove those from the list --- NOT TRUE - if it's in wrongs and yellows then remove it from wrongs
            if ug in yellows.keys() or ug in greens:
                wrongs.remove(ug)
                yellows[ug].append(index)

    # Filtering stage
    greenStr = generateGreenStr(greens)
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
    # print("after keeping only words that have proper yellows too: ", len(words))
    # print("possible words: ", len(words))
    # if len(words) > 15:
    #     print("some next guesses", sample(words, 15))
    #     happy = False
    #     while not happy:
    #         answer = input("type y to see more guesses: ")
    #         if answer != "y":
    #             happy = True
    #         else:
    #             print("some next guesses", sample(words, 15))
    # else:
    #     print("some next guesses", words)



    # input("continue")
