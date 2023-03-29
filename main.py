from data import Data
from ui import *
from question_model import Question
from quiz_brain import QuizBrain


class QuizMain:
    def __init__(self):

        while True:
            main_menu = MenuUi()   # Calling the Main Menu
            data = Data(main_menu.get_args())   # Passing the Args to API and storing the data in the data
            question_bank = []

            for question in data.question_data:       # Iterating through all the questions
                question_text = question["question"]  # and getting the question individually
                question_answer = question["correct_answer"]  # getting each answer individually
                new_question = Question(question_text, question_answer)  # getting the q/s object
                question_bank.append(new_question)

            quiz = QuizBrain(question_bank)   # Passing all the questions into the QuizzBrain

            interface = QuizUi(quiz)          # Passing the Quizz object into interface to read questions
            if interface.new_quiz:            # if the user requests for a new quiz, the quiz main resets
                self.__init__()


QuizMain()  # calling the quiz main

