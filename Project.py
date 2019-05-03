import random as r # importing random to generate a random word
from flask import *
import PyDictionary

dictionary = PyDictionary.PyDictionary() # creating dictionary object to access dictionary

# creating flask app
app = Flask(__name__)


# method to generate random word according to the level
def random_word(level):
    global victory, word, file
    if level == "Easy":
        file = open("meaning_three.txt") # opening the file containing three letter words
        victory = 3 # variable to measure the correct number of bulls
    elif level == "Medium":
        file = open("meaning_four.txt") # opening the file containing four letter words
        victory =4
    

    words = file.read().splitlines()# make all the three letter words to the list
    word = r.choice(words)# generating a random word from the list
    print(word)

# method to calculate number of cows and bulls from the given word
def calculate_cow_bull(guess):
    cow, bull = 0, 0
    for i in guess:
        if i in word:
            if word.index(i) == guess.index(i):
                bull +=1
            else:
                cow += 1
    return guess, cow, bull



result_list = []


# the first page
@app.route('/')
def start():
    return render_template("firstpage.html")




@app.route('/level',methods = ['post'])
def level():
    details = request.form
    level = details['level']
    random_word(level)
    return render_template("singleplayer.html",length = 0, result = 0)


@app.route('/howtoplay',methods = ['post'])
def howtoplay():
    f = open("howtoplay.txt")
    text = f.read()
    return render_template("howtoplay.html",text = text)

@app.route('/cowandbull', methods = ['post'])
def cow_and_bull():
    details = request.form
    guess = details['guess'] # getting the guess word
    result = list(calculate_cow_bull(guess)) # calling function to calculate no of bulls and cows
    result_list.append(result)
    length = len(result)
    if result[2] == victory:
        meaning = dictionary.meaning(word)
        return render_template("victory.html",word = word, meaning = meaning)
    else:
        return render_template("singleplayer.html",length = length, result = result_list)


app.run()  # initiating the flask app


