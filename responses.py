import random
from random import choice, randint
from typing import Final
import requests
from datetime import datetime
from fuzzywuzzy import process

# Responses
def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()
    # no message
    if lowered == '':
        return 'Well, this is awkward...'
    # hello  
    elif 'hello' in lowered:
        return 'Hello there!'
    # how are you
    elif 'how are you' in lowered:
        return 'Great, thanks!'
    # roll dice
    elif 'roll a dice' in lowered:
        return f'You rolled: {roll_dice()}'
    # flip coin
    elif 'flip a coin' in lowered:
        return f'You got: {flip_coin()}'
    # calculator
    elif 'calculate' in lowered:
        expression = lowered.replace('calculate', '', 1).strip()
        if validate_expression(expression):
            return f'The answer is: {calculator(expression)}'
        else:
            return 'Please enter a valid calculation expression.'
    # world timezone clock
    elif 'time in' in lowered:
         city = lowered.replace('time in', '', 1).strip()
         if city:
            return get_current_time(city)
         else:
             return 'Please enter a valid city name.'
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
            return 'Please enter a valid operator: +, -, *, /.'

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

# World Time API
def get_current_time(city):
    try:
        timezones_response = requests.get(f'https://worldtimeapi.org/api/timezone')
        timezones = timezones_response.json()

        # FuzzyWuzzy allows users to input 'new york' instead of 'New_York'
        best_match, match_score = process.extractOne(city, timezones, scorer = process.fuzz.partial_ratio)
        if match_score < 75:
            return 'Please enter a valid city name.'
        
        response = requests.get(f'https://worldtimeapi.org/api/timezone/{best_match}')
        data = response.json()
        datetime_object = datetime.fromisoformat(data['datetime'])
        current_time = datetime_object.strftime('%I:%M %p')
        return f'The current time in {city.title()} is: {current_time}'
    except Exception as e:
        return 'An error occurred while fetching the data.'

# Response to an unsupported message
def choose_random_response(user_input: str) -> str:
    responses: Final[str] = [
        'I do not quite understand...',
        'What are you talking about?',
        'Do you mind rephrasing that?'
    ]
    return random.choice(responses) if user_input else 'You did not say anything...'
    

