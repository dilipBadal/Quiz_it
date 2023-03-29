import time
import tkinter.messagebox
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from quiz_brain import QuizBrain

THEME_COLOR = "#375362"
WIDTH = "500"
HEIGHT = "600"


class QuizUi:
    def __init__(self, quiz=None):
        self.score = 0
        self.window = Tk()
        self.quiz = quiz
        self.new_quiz = False
        self.window.title("Know That")
        self.window.resizable(0, 0)
        self.window.geometry(f"{WIDTH}x{HEIGHT}")

        self.frame = Frame(self.window, bg=THEME_COLOR, width=500, height=600, padx=20, pady=20)
        self.frame.place(x=0, y=0)

        self.score_label = Label(self.frame, text=f"Score: {self.quiz.score}", foreground="white",
                                 bg=THEME_COLOR, font=("Arial", 15, "italic"))
        self.score_label.place(x=350, y=0)

        self.canvas = Canvas(self.frame, bg="white", width=300, height=250)
        self.canvas.place(x=80, y=150)
        self.question = self.canvas.create_text(150, 125, width=280, text="Question Here", fill="black", font=("Arial", 12, "normal"))

        img_wrong = ImageTk.PhotoImage(Image.open("images/false.png"))
        self.wrong = Button(self.frame, image=img_wrong, highlightthickness=0, command=self.pressed_wrong)
        self.wrong.place(x=80, y=450)

        img_right = ImageTk.PhotoImage(Image.open("images/true.png"))
        self.right = Button(self.frame, image=img_right, highlightthickness=0, command=self.pressed_right)
        self.right.place(x=270, y=450)

        self.get_question()
        self.wrong.config(state=ACTIVE)
        self.right.config(state=ACTIVE)
        self.window.mainloop()

    def get_question(self):
        if self.quiz.still_has_questions():
            self.canvas.config(bg="white")
            self.canvas.itemconfig(self.question, text=self.quiz.next_question())
            self.wrong.config(state=ACTIVE)
            self.right.config(state=ACTIVE)
        else:
            self.wrong.config(state=DISABLED)
            self.right.config(state=DISABLED)
            self.canvas.config(bg="white")
            reset = Button(self.frame, text="Menu", font=("Arial", 10, "normal"), highlightthickness=0, bg="lightblue",
                           command=self.reset_quiz)
            reset.place(x=80, y=110)
            self.canvas.itemconfig(self.question, text=f"You've finished the Quiz!")
            self.canvas.create_text(150, 145, width=280, text=f"Your Score: {self.quiz.score}", fill="black",
                                    font=("Arial", 15, "normal"))

    def reset_quiz(self):
        self.window.destroy()
        self.new_quiz = True

    def pressed_wrong(self):
        self.wrong.config(state=DISABLED)
        is_correct = self.quiz.check_answer("false")
        self.score_label.config(text=f"Score: {self.quiz.score}")
        self.give_feedback(is_correct)

    def pressed_right(self):
        self.right.config(state=DISABLED)
        is_correct = self.quiz.check_answer("true")
        self.score_label.config(text=f"Score: {self.quiz.score}")
        self.give_feedback(is_correct)

    def give_feedback(self, is_correct):
        if is_correct:
            self.canvas.config(bg="green")
        else:
            self.canvas.config(bg="red")

        self.canvas.update()
        self.window.after(1000, self.get_question())


class MenuUi:
    def __init__(self):
        self.score = 0
        self.window = Tk()
        self.window.title("Know That")
        self.window.resizable(0, 0)
        self.window.geometry(f"{WIDTH}x{HEIGHT}")
        self.args = {}
        self.frame = Frame(self.window, bg=THEME_COLOR, width=500, height=600, padx=20, pady=20)
        self.frame.place(x=0, y=0)
        title = Label(self.frame, text="Know That", font=("Arial", 50, "italic"), bg=THEME_COLOR, foreground="lightblue")
        title.place(x=70, y=50)
        self.play = Button(self.frame, highlightthickness=0, text="Play", width=15, height=2, bg="green",
                      font=("Arial", 10, "italic"), command=self.choose_quiz_menu)
        self.play.place(x=160, y=250)

        self.quit = Button(self.frame, highlightthickness=0, text="Quit", width=15, height=2, bg="red",
                      font=("Arial", 10, "italic"), command=self.end_it)
        self.quit.place(x=160, y=350)
        self.category_combo = None
        self.difficulty_combo = None
        self.questions_text = None
        self.next = None
        self.window.mainloop()

    def get_args(self):   # Returns the arguments for the API
        return self.args

    def end_it(self):     # Ends the Quiz by destroying the current Window
        self.window.destroy()

    def choose_quiz_menu(self):   # Method to choose the type of QUIZ
        self.frame.destroy()
        self.frame = Frame(self.window, bg=THEME_COLOR, width=500, height=600, padx=20, pady=20)
        self.frame.place(x=0, y=0)
        title = Label(self.frame, text="Know That", font=("Arial", 50, "italic"), bg=THEME_COLOR,
                      foreground="lightblue")
        title.place(x=70, y=50)

        category_label = Label(self.frame, text="Select Category", font=("Microsoft YaHei UI Light", 15, "normal"), bg=THEME_COLOR,
                               foreground="lightblue")
        category_label.place(x=60, y=240)
        values = ["Select Category", "Sports", "History", "Computers", "Vehicles"]
        self.category_combo = ttk.Combobox(self.frame, values=values)
        self.category_combo.place(x=220, y=250)
        self.category_combo.set(values[0])

        difficulty_label = Label(self.frame, text="Select Difficulty", font=("Microsoft YaHei UI Light", 15, "normal"),
                                 bg=THEME_COLOR, foreground="lightblue")
        difficulty_label.place(x=60, y=340)
        values = ["Select Difficulty", "Easy", "Medium", "Hard"]
        self.difficulty_combo = ttk.Combobox(self.frame, values=values)
        self.difficulty_combo.place(x=220, y=350)
        self.difficulty_combo.set(values[0])

        questions_label = Label(self.frame, text="No. Questions", font=("Microsoft YaHei UI Light", 15, "normal"),
                                bg=THEME_COLOR, foreground="lightblue")
        questions_label.place(x=60, y=440)
        self.questions_text = Entry(width=18, fg="black", border=0, font=("Microsoft YaHei UI Light", 11))
        self.questions_text.place(x=238, y=465)

        self.next = Button(self.frame, highlightthickness=0, text="Next", width=15, height=2, bg="green",
                           font=("Arial", 10, "italic"), command=self.set_args)
        self.next.place(x=160, y=500)

    def set_args(self):   # Method to create arguments for the API

        if self.questions_text.get() <= "" or int(self.questions_text.get()) <= 0 or self.category_combo.get() == "Select Category" or self.difficulty_combo.get() == "Select Difficulty":
            tkinter.messagebox.showerror("Error", "Invalid Inputs")
            return None

        categories = {
            "Sports": 21,
            "History": 23,
            "Computers": 18,
            "Vehicles": 28,
        }

        cat_value = 0
        for i in categories.items():
            if i[0] == self.category_combo.get():
                cat_value = i[1]

        self.args = {
            "amount": self.questions_text.get(),
            "category": cat_value,
            "difficulty": self.difficulty_combo.get().lower(),
            "type": "boolean",
        }

        self.window.destroy()