import pandas
import json
from random import choice
from tkinter import *

words_guessed_correctly = []
current_word = {}
dicts = []
timer = NONE

#-------------Words----------------#


try:
    to_learn_data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    dicts = original_data.to_dict(orient="records")
else:
    dicts = to_learn_data.to_dict(orient="records")
finally:
    translation_dicts = {word["French"]: word["English"] for word in dicts}


#--------------Cards---------------#


def generate_card():
    global current_word
    valid_words = [item for item in translation_dicts.items() if item not in words_guessed_correctly]
    current_word = choice(valid_words)
    card_canvas.itemconfig(card_image, image=card_back)
    card_canvas.itemconfig(language_text, text="French")
    card_canvas.itemconfig(word_text, text=current_word[0])
    window.after(3000, flip_card)
    correct_button.config(command=NONE)
    incorrect_button.config(command=NONE)


def flip_card():
    card_canvas.itemconfig(card_image, image=card_front)
    card_canvas.itemconfig(language_text, text="English")
    card_canvas.itemconfig(word_text, text=current_word[1])
    correct_button.config(command=correct_guess)
    incorrect_button.config(command=incorrect_guess)


#------------interface-------------#


def correct_guess():
    words_guessed_correctly.append(current_word)
    words_to_learn = [item for item in translation_dicts.items() if item not in words_guessed_correctly]
    new_data = pandas.DataFrame(words_to_learn, columns=["French", "English"])
    new_data.to_csv("data/words_to_learn.csv", index=False)
    generate_card()


def incorrect_guess():
    generate_card()


#---------------UI-----------------#


BACKGROUND_COLOR = "#B1DDC6"

window = Tk()
window.config(width=800, height=626, padx=50, pady=50, background=BACKGROUND_COLOR)
window.title("Flash Cards")


card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")

card_canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_image = card_canvas.create_image(400, 268, image=card_front)
card_canvas.grid(row=0, column=0, columnspan=2)
language_text = card_canvas.create_text(400, 150, text="Language", font=("Arial", 40, "italic"))
word_text = card_canvas.create_text(400, 263, text="Word", font=("Arial", 60, "bold"))

incorrect_image = PhotoImage(file="images/wrong.png")
correct_image = PhotoImage(file="images/right.png")
incorrect_button = Button(image=incorrect_image, highlightthickness=0, command=incorrect_guess)
correct_button = Button(image=correct_image, highlightthickness=0, command=correct_guess)

incorrect_button.grid(row=1, column=0)
correct_button.grid(row=1, column=1)

generate_card()

window.mainloop()
