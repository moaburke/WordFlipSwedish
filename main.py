"""
Flash Card Learning Application

Author: Moa Burke
Date: 19 Oct 2024
Description:
    The program implements a flash card learning application using Python and Tkinter for the graphical user interface (GUI).
    Users can learn Swedish vocabulary by flipping cards to view both the Swedish word and its English translation.
    The application selects random words from a list, allows users to mark words as known, and tracks learning progress
    by maintaining a count of total guesses and correct guesses.
    Progress is saved to a CSV file, allowing users to resume their learning later.
    Once all words have been mastered, users have the option to restart their learning journey.
    Appropriate error handling has been implemented for file operations to ensure smooth functionality when loading
    or saving progress.

Version: 1.0

Changelog:
    - 1.0:  Initial version with core features including random word selection, card flipping,
            tracking of correct guesses, saving progress to a CSV file, basic error handling,
            and the option for users to restart their learning journey after mastering all words.
"""


from tkinter import *
import random
import pandas
from pandas.errors import EmptyDataError

# Constants for colors used in the UI
BACKGROUND_COLOR = "#142638"
DARK_BLUE = "#142638"
WHITE = "#fafafa"
YELLOW = "#fecb00"
DARK_YELLOW = "#e3aa0e"

# Constant for font name
FONT_NAME = "Bahnschrift SemiLight Condensed"

# File path constants for CSV files
WORDS_TO_LEARN = "./data/words_to_learn.csv"
SWEDISH_WORDS_FILE = "./data/swe_words.csv"

# Image constants for the card and buttons
CARD_FRONT = "./images/card_front.png"
CARD_BACK = "./images/card_back.png"
WRONG_BUTTON = "./images/wrong.png"
RIGHT_BUTTON = "./images/right.png"

# Dictionary to store words that user has to learn
to_learn = {}
# Dictionary to store the current word being displayed
current_word = {}

# Counters to track total number of words guessed and correct guesses
total_words_guessed = 0
total_correct_guesses = 0


# Attempt to load saves progress, fall back to original data if the file doesn't exist or is empty
try:
    data = pandas.read_csv(WORDS_TO_LEARN) # Load progress from CSV file
except FileNotFoundError:
    # If file doesn't exist, load the original data
    original_data = pandas.read_csv(SWEDISH_WORDS_FILE)
    to_learn = original_data.to_dict(orient='records') # Convert to dictionary
except EmptyDataError:
    # Handle the case where the CVS is empty
    original_data = pandas.read_csv(SWEDISH_WORDS_FILE)
    to_learn = original_data.to_dict(orient='records') # Convert to dictionary
else:
    # Convert data to a list of dictionaries for easy access
    to_learn = data.to_dict(orient='records')  # Convert to dictionary

def next_card():
    """
    Selects a random word from the list to learn and updates the UI to display the Swedish word.
    Set a timer to flip the card and show the English translation after 3 seconds.
    """
    global current_word, flip_timer, total_words_guessed, to_learn

    # Cancel the current active timer (if any) to prevent multiple card flips at the same time
    window.after_cancel(flip_timer)

    try:
        current_word = random.choice(to_learn) # Select a random word from the list
    except IndexError:
        # If the list with words to learn are empty, and all words are learned, display a completion message
        all_completed()
    else:
        # Extract the Swedish word from the current dictionary
        word_swedish = current_word["Swedish"]

        # Update the canvas with the Swedish word and UI elements
        canvas.itemconfig(card_title, text="Swedish", fill=DARK_YELLOW) # Set the card title to "Swedish" with yellow text
        canvas.itemconfig(card_word, text=word_swedish, fill=DARK_BLUE, font=(FONT_NAME, 80, "bold")) # Display the Swedish word with dark blue text

        # Update the canvas to display the number of correct guesses out of the total words guessed
        canvas.itemconfig(card_correct_guesses, text=f"{total_correct_guesses}/{total_words_guessed} correct words", fill=DARK_BLUE)

        canvas.itemconfig(canvas_img, image=card_front_img) # Update the canvas image to show the front of the card (Swedish word)

        # Increment the total number of words guessed
        total_words_guessed += 1

        # Set a timer to flip the card to the English translation after 3 seconds
        flip_timer = window.after(3000, func=flip_card)

def flip_card():
    """
    Flips the current card to show the English translation of the word.
    Updates the canvas to display the English word.
    """
    word_english = current_word["English"]  # Extract the English translation of the word

    # Update the canvas to show the back of the card with the English word
    canvas.itemconfig(canvas_img, image=card_back_img) # Change the canvas image to show the back of the card (English word)
    canvas.itemconfig(card_title, text="English", fill=YELLOW)  # Change card title to "English"
    canvas.itemconfig(card_word, text=word_english, fill=WHITE)  # Display the English word
    canvas.itemconfig(card_correct_guesses, fill=WHITE) # Update the color of the text displaying guesses

def known_word():
    """
    Marks the current word as known, removes it from the list,
    updates the progress in the CSV file, and moves to the next word.
    """
    global total_correct_guesses
    total_correct_guesses += 1 # Increment for correct guesses

    try:
        to_learn.remove(current_word) # Remove the known word from the list
    except ValueError:
        # Handle case where the list is empty
        all_completed()
    else:
        # Save the progress to the CSV file
        progress_data = pandas.DataFrame(to_learn)
        progress_data.to_csv(WORDS_TO_LEARN, index=False)

        # Move to the next card
        next_card()

def all_completed():
    """
    Displays a message indicating that the user has learned all words.
    """
    global restart_button
    # Update the canvas to display a congratulatory message
    canvas.itemconfig(card_title, text="Congratulations!", fill=DARK_YELLOW)
    canvas.itemconfig(card_word, text="You have learned all words.", fill=DARK_BLUE, font=(FONT_NAME, 45, "bold"))
    canvas.itemconfig(card_correct_guesses, text="") # Clear the correct guesses text

    # Display the "restart" button on the screen, allowing the user to re-start the learning
    restart_button.place(x=280, y=410)

def start_over():
    """
    Resets the progress and starts the learning process from the beginning.
    """
    global to_learn, total_correct_guesses, total_words_guessed, restart_button

    # Load the original word list from the CSV file
    words_data = pandas.read_csv(SWEDISH_WORDS_FILE)
    to_learn = words_data.to_dict(orient='records')

    # Hide the restart button
    restart_button.place(x=-1000, y=-1000)

    # Reset the counter for total words guessed and correct guesses
    total_words_guessed = 0
    total_correct_guesses = 0

    # Start with the first card
    next_card()


# Main window setup
window = Tk() # Create a new Tkinter window
window.title("Learn Swedish by Moa Burke") # Set window title
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR) # Configure padding and background color

# Start a timer to flip the card after 3 seconds. Once the timer runs out,
# the 'flip_card' function will be called to show the English translation
flip_timer = window.after(3000, func=flip_card)

# Create canvas to display the card
canvas = Canvas(width=800, height=600, highlightthickness=0, bg=BACKGROUND_COLOR) # Create a canvas widget
card_front_img = PhotoImage(file=CARD_FRONT) # Load the front card image
card_back_img = PhotoImage(file=CARD_BACK) # Load the back card image
canvas_img = canvas.create_image(400, 300, image=card_front_img) # Add the image to the canvas

# Create text elements on the canvas
card_top= canvas.create_text(200, 15, text="Swedish Words for Everyday Life", font=(FONT_NAME, 25), fill=WHITE)
card_title = canvas.create_text(400, 170, text="", font=(FONT_NAME, 30), fill=YELLOW)
card_word = canvas.create_text(400, 280, text="", font=(FONT_NAME, 80, "bold"))
card_correct_guesses = canvas.create_text(400, 480, font=(FONT_NAME, 18))
canvas.grid(row=0, column=0, columnspan=2)

# Button for wrong answers
wrong_img = PhotoImage(file=WRONG_BUTTON) # Load the image for wrong button
wrong_button = Button(image=wrong_img, command=next_card, highlightthickness=0, borderwidth=0)
wrong_button.grid(row=1, column=0)

# Button for correct answers
right_img = PhotoImage(file=RIGHT_BUTTON) # Load the image for right button
right_button = Button(image=right_img, command=known_word, highlightthickness=0, borderwidth=0)
right_button.grid(row=1, column=1)

# Create a button to reset the progress and restart the learning session
# It will only be displayed when all words have been mastered
restart_button = Button(text="Restart Learning", command=start_over, width="20", bg=DARK_YELLOW, fg=WHITE, font=(FONT_NAME, 18, "bold"))

# Initialize the first card
next_card()

# Start the Tkinter event loop
window.mainloop() # Keep the window open until manually closed