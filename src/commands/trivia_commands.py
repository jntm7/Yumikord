import requests
import random
import html

# Trivia
class TriviaGame:
    def __init__(self):
        self.active_game = False
        self.question = None
        self.correct_answer = None
        self.all_answers = []

    def get_trivia_question(self):
        response = requests.get("https://opentdb.com/api.php?amount=1&type=multiple")
        data = response.json()
        if data['response_code'] == 0:
            question_data = data['results'][0]
            self.question = html.unescape(question_data['question'])
            self.correct_answer = html.unescape(question_data['correct_answer'])
            incorrect_answers = [html.unescape(answer) for answer in question_data['incorrect_answers']]
            self.all_answers = incorrect_answers + [self.correct_answer]
            random.shuffle(self.all_answers)
            return self.question, self.all_answers
        else:
            return None, None

    def start_game(self):
        if not self.active_game:
            self.active_game = True
            return self.get_trivia_question()
        return None, None

    def answer_question(self, answer_index):
        if self.active_game:
            if 0 <= answer_index < len(self.all_answers):
                selected_answer = self.all_answers[answer_index]
                if selected_answer == self.correct_answer:
                    self.active_game = False
                    return True, "Congratulations, that is the correct answer!"
                else:
                    self.active_game = False
                    return True, f"Sorry, the correct answer is: {self.correct_answer}"
            else:
                return False, "Please respond with a valid number."
        else:
            return False, "There is no active game. Please start a new game with `play.trivia`."