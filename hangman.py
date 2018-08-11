#HANGMAN GAME using TKINTER as a GUI

from tkinter import *
import random
import pandas as pd

class Application(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        """creating the widgets for the GUI"""

        self.letters = " -abcdefghijklmnopqrstuvwxyz"
        self.letters_list = list(self.letters)
        self.counter = 10 #counter allows you to only have 10 tries until hangman game over

        path = 'words.xlsx'
        dataframe = pd.read_excel(path) #this creates the dataframe containing the words
        self.easy_column = dataframe.iloc[: , 0] #the first column is easy words
        self.hard_column = dataframe.iloc[: , 1] #the second column is hard words

        #string variable created for two buttons below for Easy or Hard words
        self.difficulty = StringVar()
        self.difficulty.set('easy') #setting the default value to Easy
        Radiobutton(self,
                    text = "easy",
                    variable = self.difficulty,
                    value = "easy"
                    ).grid(row = 0, column = 0, sticky = W)

        Radiobutton(self,
                    text = "hard",
                    variable = self.difficulty,
                    value = "hard"
                    ).grid(row = 0, column = 1, sticky = W)

        #create button to play game - and open up the rest of the GUI
        self.bttn1 = Button(self, text = "PLAY / RESET", command = self.play_game)
        self.bttn1.grid(row = 0, column = 2, sticky = E)


    def play_game(self):
        """creation of the rest of GUI and the word is chosen"""

        #creating label that tells you to guess the word
        self.lbl1 = Label(self, text="Guess this word:")
        self.lbl1.grid(row = 2, column = 0, sticky = W)

        #creating label that tells you to press enter for guess
        self.lbl1_1 = Label(self, text="Guess a LETTER and press ENTER:")
        self.lbl1_1.grid(row = 4, column = 0, sticky = W)


        #choosing the word from the text files based on difficulty chosen randomly
        if self.difficulty.get() == 'easy':
            self.word = random.choice(self.easy_column)
        elif self.difficulty.get() == 'hard':
            self.word = random.choice(self.hard_column)

        #showing intial solution as dashes based on the length of the word
        self.solution = "-" * (len(self.word))
        self.solution_list = list(self.solution)

        #displaying this solution as a label on the GUI
        self.lbl2 = Label(self, text = self.solution)
        self.lbl2.grid(row = 2, column = 1, sticky = W)

        self.lbl3_1 = Label(self, text = "Letters left to guess: ")
        self.lbl3_1.grid(row = 3, column = 0, sticky = W)

        self.lbl3_2 = Label(self, text = "".join(self.letters_list))
        self.lbl3_2.grid(row = 3, column = 1, sticky = W)

        #user entry area to enter guesses
        self.ent = Entry(self)
        self.ent.grid(row = 4, column = 1, sticky = W)

        self.ent.bind('<KeyPress>', self.keyboard)
        self.ent.focus_set()

        self.lbl4 = Label(self, text = "Guesses left:")
        self.lbl4.grid(row = 5, column = 0, sticky = W)

        self.lbl5 = Label(self, text = str(self.counter))
        self.lbl5.grid(row = 5, column = 1, sticky = W)



    def guess_char(self):
        print(self.word) #cheat - so you can see the word in the shell
        print("".join(self.solution_list))

        #getting the guess from the user and then clearing the area
        guess = self.ent.get()
        self.ent.delete(0, END)

        if self.counter > 1:
            #temp state made to compare later to see if guess revealed anything
            temp_state = self.solution_list.copy()

            #checking if guess is in word and revealing it if so
            for i in range(len(self.word)):
                if self.word[i].upper() == guess.upper():
                    self.solution_list[i] = self.word[i]
            self.lbl2["text"] = "".join(self.solution_list)

            #checking if player has won
            if self.word == "".join(self.solution_list):
                self.lbl5["text"] = "You win at hangman!"

            #removing words from available letters to guess from
            elif guess in self.letters_list:
                self.letters_list.remove(guess)
                self.lbl3_2["text"] = "".join(self.letters_list)

                #if they made a guess, and no word was revealed
                if temp_state == self.solution_list:
                    self.counter -= 1
                    self.lbl5["text"] = self.counter

            else:
                self.lbl5["text"] = str(self.counter) + " - You've already guessed that letter."

        else:
            self.lbl2["text"] = "You lose. The word you were looking for: " + self.word
            self.lbl5["text"] = "Game Over."



    def keyboard(self, event):
        #allowing the keyboard enter stroke to make a guess
        if event.keysym == "Return":
            self.guess_char()

# main
root = Tk()
root.title("Hangman")
root.geometry("500x150")
root.resizable(width = FALSE, height = FALSE)

app = Application(root)
root.mainloop()
