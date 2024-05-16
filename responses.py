import random
from random import choice, randint
from typing import Final

# Responses
def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()
    
    if lowered == '': # Response to no message sent
        return 'Well, this is awkward...'  
    elif 'hello' in lowered:
        return 'Hello there!'
    elif 'how are you' in lowered:
        return 'Great, thanks!'
    elif 'roll a dice' in lowered:
        return f'You rolled: {roll_dice()}'
    elif 'flip a coin' in lowered:
        return f'You got: {flip_coin()}'
    elif 'calculate' in lowered:
        expression = lowered.replace('calculate', '', 1).strip()
        if validate_expression(expression):
            return f'The answer is: {calculator(expression)}'
        else:
            return 'Please provide a valid calculation expression.'
    else:
        return choose_random_response(lowered)      

# Roll a dice
def roll_dice() -> int:
    return random.randint(1,6)

# Flip a coin
def flip_coin() -> str:
    return random.choice(['heads', 'tails'])

# Calculator
def calculator(user_input: str) -> str:
    tokens = user_input.split()
    try:
        num1 = float(tokens[0])
        operator = tokens[1]    
        num2 = float(tokens[2])

        # Operations
        if operator == '+':
            result = num1 + num2
        elif operator == '-':
            result = num1 - num2
        elif operator == '*':
            result = num1 * num2
        elif operator == '/':
            # if user tries to divide by zero
            if num2 == 0: 
                return 'Division by zero is not possible.'
            result = num1 / num2
        else:
            return 'Please enter one of the following operators: +, -, *, /.'

        # Integer or Float output depending on input
        if isinstance(num1, int) and isinstance(num2, int): 
            return f'{int(result)}'  # Return integer result
        else:
            return f'{result}'  # Return float result

    # if user enters invalid float
    except ValueError:
        return 'Please enter valid numbers for calculation.'

def validate_expression(expression: str) -> bool:
    # Validates if the expression contains at least one number and one operator
    return any(char.isdigit() for char in expression) and any(char in expression for char in ['+', '-', '*', '/'])

# Response to an unsupported message
def choose_random_response(user_input: str) -> str:
    responses: Final[str] = [
        'I do not quite understand...',
        'What are you talking about?',
        'Do you mind rephrasing that?'
    ]
    return random.choice(responses) if user_input else 'You did not say anything...'
    

