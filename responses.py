import random
from random import choice, randint
from typing import Final

# Responses
def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()
    
    if lowered == '': #Response to no message sent
        return 'Well, this is awkward...'  
    elif 'hello' in lowered:
        return 'Hello there!'
    elif 'how are you' in lowered:
        return 'Great, thanks!'
    elif 'roll a dice' in lowered:
        return f'You rolled: {roll_dice()}'
    elif 'flip a coin' in lowered:
        return f'You got: {flip_coin(user_input)}'
    elif 'calculate' in lowered:
        return calculator(lowered)
    else:
        return choose_random_response(lowered)  

# Roll a dice
def roll_dice() -> int:
    return random.randint(1,6)

# Flip a coin
def flip_coin() -> str:
    result = random.choice(['heads', 'tails'])

# Calculator
def calculator(user+input: str) -> str:
    tokens = user_input.split()

    if len(tokens) != 3 ## len = length of a sequence
        return "Please provide a function in the format of <number> <operator> <number>"
    try:
        x = float(tokens[0])
        operator = tokens[1]
        y = float(tokens[2])
        #Operations
        if operator == '+':
            result = x + y
        elif operator == '-':
            result = x - y
        elif operator == '*':
            result = x * y
        elif operator == '/':
            # if user tries to divide by zero
            if y == 0: 
                return "Division by zero is not possible."
            result = num1 / num2
        else:
            return "Please enter one of the following operators: +, -, *, /."
        return f'Result: {result}'
    # If user enters invalid float
    except ValueError:
        return "Please enter valid numbers for calculation."
        
#Response to an unsupported message
def choose_random_response(user_input: str) -> str:
    responses: Final[str] = [
        'I do not quite understand...',
        'What are you talking about?',
        'Do you mind rephrasing that?'
    ]
    return random.choice(responses) if user_input else 'You did not say anything...'
    

