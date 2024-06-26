import random

game_states = {}

# Rock Paper Scissors Logic
def play_rps(user_id, user_choice):
    choices = ['rock', 'paper', 'scissors']
    if user_choice not in choices:
        return "Invalid choice. Please choose rock, paper, or scissors."
    
    bot_choice = random.choice(choices)
    if user_choice == bot_choice:
        return f"Both chose {user_choice}. It's a tie!"
    elif (user_choice == "rock" and bot_choice == "scissors") or \
         (user_choice == "paper" and bot_choice == "rock") or \
         (user_choice == "scissors" and bot_choice == "paper"):
        return f"You chose {user_choice} and I chose {bot_choice}. You win!"
    else:
        return f"You chose {user_choice} and I chose {bot_choice}. I win!"

# Number Guesser Game Initialization
def start_guesser(user_id):
    secret_number = random.randint(1, 100)
    game_states[user_id] = {'number': secret_number, 'attempts': 0, 'max_attempts': 8}
    return "I've chosen a number between 1 and 100. Can you guess it? You have 8 chances. Let's start!"

# Number Guesser Logic
def play_guesser(user_id, guess):
    if user_id not in game_states:
        return "Please start a new game using !start_guesser."
    
    game_state = game_states[user_id]
    secret_number = game_state['number']
    attempts = game_state['attempts'] + 1

    if attempts >= game_state['max_attempts']:
        del game_states[user_id]
        return f"Sorry, you've run out of attempts. The number was {secret_number}."
    
    game_state['attempts'] = attempts
    if guess < secret_number:
        return "Higher..."
    elif guess > secret_number:
        return "Lower..."
    else:
        del game_states[user_id]
        return "Congratulations! You've guessed the number!"