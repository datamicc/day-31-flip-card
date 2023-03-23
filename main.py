BACKGROUND_COLOR = "#B1DDC6"
to_learn = {}
current_card = {}

from tkinter import *
import pandas
import random
#----------------READ DATA FROM FILE----------------------------


try:
    df = pandas.read_csv('data/words_to_learn.csv')
except FileNotFoundError:
    original_data = pandas.read_csv('data/french_words.csv')
    to_learn = original_data.to_dict(orient='records')
else:
    to_learn = df.to_dict(orient='records')


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text='French', fill='black')
    canvas.itemconfig(card_word, text=current_card['French'], fill='black')
    canvas.itemconfig(card_image, image=front_image)
    flip_timer = window.after(3000, func=flip_card)

def flip_card():
    global current_card
    canvas.itemconfig(card_title, text='English', fill='white')
    canvas.itemconfig(card_image, image=back_image)
    canvas.itemconfig(card_word, text=current_card['English'], fill='white')

def correct_guess():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv('data/words_to_learn.csv', index=False)
    next_card()

#----------------SETUP UI----------------------------
window = Tk()
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)
window.title('Flashy')

flip_timer = window.after(3000, func=flip_card)

front_image = PhotoImage(file='images/card_front.png')
back_image = PhotoImage(file='images/card_back.png')

canvas = Canvas(bg=BACKGROUND_COLOR, width=800, height=526, highlightthickness=0)
card_image = canvas.create_image(410, 270, image=front_image)
card_title = canvas.create_text(400, 150, font=('Ariel', 40, 'italic'), text='title')
card_word = canvas.create_text(400, 253, font=('Ariel', 60, 'bold'), text='word')
canvas.grid(column=0, row=0, columnspan=2)


wrong_image = PhotoImage(file='images/wrong.png')
wrong_button = Button(image=wrong_image, highlightthickness=0, command=next_card)
wrong_button.grid(column=0, row=1)

right_image = PhotoImage(file='images/right.png')
right_button = Button(image=right_image, highlightthickness=0, command=correct_guess)
right_button.grid(column=1, row=1)


next_card()



window.mainloop()