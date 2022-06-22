import random
from tkinter import *
import pandas as pd

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

try:
    data = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pd.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="record")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(card_image, image=card_front_image)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_image, image=card_back_image)


def is_known():
    to_learn.remove(current_card)
    data = pd.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


# ---- UI design ---- #
window = Tk()
window.title("Flashy")
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=480, highlightthickness=0, bg=BACKGROUND_COLOR)
card_front_image = PhotoImage(file="images/card_front.png")
card_back_image = PhotoImage(file="images/card_back.png")
card_image = canvas.create_image(400, 240, image=card_front_image)
card_title = canvas.create_text(400, 140, text="Title", fill="Black", font=("Arial", 40, "italic"))
card_word = canvas.create_text(400, 240, text="Word", fill="Black", font=("Arial", 60, "bold"))
canvas.grid(row=1, column=1, columnspan=2)

cross_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=cross_image, highlightthickness=0, background=BACKGROUND_COLOR, pady=2, padx=2,
                        command=next_card)
unknown_button.grid(row=2, column=1)

right_image = PhotoImage(file="images/right.png")
known_Button = Button(image=right_image, highlightthickness=0, background=BACKGROUND_COLOR, pady=2, padx=2,
                      command=is_known)
known_Button.grid(row=2, column=2)

next_card()
window.mainloop()
