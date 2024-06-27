import random

game_states = {}

# Dice Roll Logic
def roll_dice():
    result = random.randint(1, 6)
    return f"You rolled: {result}"

# Coin Flip Logic
def flip_coin():
    result = random.choice(['heads', 'tails'])
    return f"The coin landed on: {result}"

# Random Number Generator Logic
def generate_random_number(min_val: int, max_val: int):
    result = random.randint(min_val, max_val)
    return f"Your random number is: {result}"

# Rock Paper Scissors Logic
def play_rps(user_id, user_choice):
    choices = ['rock', 'paper', 'scissors']
    if user_choice not in choices:
        return "Invalid choice. Please choose rock, paper, or scissors."
    
    # Check if there's an ongoing game for the user
    if user_id in game_states and game_states[user_id]['active']:
        return "You already have an ongoing game. Please finish it before starting a new one."
    
    bot_choice = random.choice(choices)
    result = ""
    if user_choice == bot_choice:
        result = f"Both chose {user_choice}. It's a tie!"
    elif (user_choice == "rock" and bot_choice == "scissors") or \
         (user_choice == "paper" and bot_choice == "rock") or \
         (user_choice == "scissors" and bot_choice == "paper"):
        result = f"You chose {user_choice} and I chose {bot_choice}. You win!"
    else:
        result = f"You chose {user_choice} and I chose {bot_choice}. I win!"
    
    game_states[user_id] = {'active': False, 'last_result': result}
    return result

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