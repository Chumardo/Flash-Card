from tkinter import *
from tkinter import messagebox
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}
to_learn_geo = {}
language = ""


def show_info():
    messagebox.showinfo(title="Guess word on English", message="You have only 3 seconds.\nIf you guess choose check mark, if didn't choose 'x'.")


def lang_geo():
    global language
    language = "Georgian"
    next_card()


def lang_french():
    global language
    language = "French"
    next_card()
    
def lang_russian():
    global language
    language = "Russian"
    next_card()



try:
    data = pandas.read_csv(".//data/words_to_learn.csv")
    # data = pandas.read_csv(".//data/words_to_learn_geo.csv")
except FileNotFoundError:
    if language == "":
        try:
            data = pandas.read_csv(".//data/words_to_learn_geo.csv")
            to_learn_geo = data.to_dict(orient="records")
        except FileNotFoundError:
            original_data_geo = pandas.read_csv(".//data/English-words-Sheet1.csv")
            original_data = pandas.read_csv(".//data/french_russian_words.csv")
            to_learn = original_data.to_dict(orient="records")
            to_learn_geo = original_data_geo.to_dict(orient="records")
    elif language == "Russian" or language == "French":
        original_data = pandas.read_csv(".//data/french_russian_words.csv")
        to_learn = original_data.to_dict(orient="records")
else:
    original_data_geo = pandas.read_csv(".//data/English-words-Sheet1.csv")
    to_learn_geo = original_data_geo.to_dict(orient="records")
    if language == "Georgian":
        original_data_geo = pandas.read_csv(".//data/English-words-Sheet1.csv")
        to_learn_geo = original_data_geo.to_dict(orient="records")
    else:
        original_data = pandas.read_csv(".//data/french_russian_words.csv")
        to_learn = original_data.to_dict(orient="records")
    

def next_card():
    global current_card, flip_timer
    if language == "Georgian":
        global current_card, flip_timer
        window.after_cancel(flip_timer)
        current_card = random.choice(to_learn_geo)
        try:
            canvas.itemconfig(card_title, text=language, fill="black")
            canvas.itemconfig(card_word, text=current_card[language], fill="black")
        except KeyError:
            canvas.itemconfig(card_title, text="Choose", fill="black")
            canvas.itemconfig(card_word, text="language", fill="black")
        else:
            canvas.itemconfig(card_background, image=front_image)
            flip_timer = window.after(5000, func=flip_card)       
    else:
        window.after_cancel(flip_timer)
        current_card = random.choice(to_learn)
        try:
            canvas.itemconfig(card_title, text=language, fill="black")
            canvas.itemconfig(card_word, text=current_card[language], fill="black")
        except KeyError:
            canvas.itemconfig(card_title, text="Choose", fill="black")
            canvas.itemconfig(card_word, text="language", fill="black")
        else:
            canvas.itemconfig(card_background, image=front_image)
            flip_timer = window.after(5000, func=flip_card)
    
    
def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    try:
        canvas.itemconfig(card_word, text=current_card["English"], fill="white")
        canvas.itemconfig(card_background, image=back_image)
    except:
        canvas.itemconfig(card_title, text="Choose", fill="black")
        canvas.itemconfig(card_background)
        


def is_known():
    if language == "Georgian":
        to_learn_geo.remove(current_card)
        data = pandas.DataFrame(to_learn_geo)
        data.to_csv("data/words_to_learn_geo.csv", index=False)
        next_card()
    else:
        to_learn.remove(current_card)
        data = pandas.DataFrame(to_learn)
        data.to_csv("data/words_to_learn.csv", index=False)
        next_card()

window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)


flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
front_image = PhotoImage(file=".//images/card_front.png")
back_image = PhotoImage(file=".//images/card_back.png")
card_background = canvas.create_image(400, 263, image=front_image)
card_title = canvas.create_text(400, 150, text="Choose", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="language", font=("Ariel", 40, "bold"))
canvas.grid(column=1, row=1, columnspan=2)


wrong_image = PhotoImage(file=".//images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, bg=BACKGROUND_COLOR, command=next_card)
wrong_button.grid(column=1, row=2)

right_image = PhotoImage(file=".//images/right.png")
right_button = Button(image=right_image, highlightthickness=0, bg=BACKGROUND_COLOR, command=is_known)
right_button.grid(column=2, row=2)

french_image = PhotoImage(file=".//images/france.png")
french_button = Button(image=french_image, bg=BACKGROUND_COLOR, command=lang_french, height=30, width=30)
french_button.grid(column=1, row=0, padx=10, pady=10, columnspan=2)

russian_image = PhotoImage(file=".//images/russia.png")
russian_button = Button(image=russian_image, bg=BACKGROUND_COLOR, command=lang_russian, height=30, width=30)
russian_button.grid(column=2, row=0, padx=10, pady=10)

geo_image = PhotoImage(file=".//images/georgia.png")
geo_button = Button(image=geo_image, bg=BACKGROUND_COLOR, command=lang_geo)
geo_button.grid(column=1, row=0)


info_image = PhotoImage(file=".//images/info.png")
info_button = Button(image=info_image, bg=BACKGROUND_COLOR, command=show_info)
info_button.grid(column=1, row=2, columnspan=2)





# next_card()

window.mainloop()