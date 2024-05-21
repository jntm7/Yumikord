import random
from random import choice, randint
from typing import Final
import requests
from datetime import datetime
from fuzzywuzzy import process
from googletrans import Translator
translator = Translator()

conversion_factors = {
    'miles_to_km': 1.60934,
    'km_to_miles': 0.621371,
    'inches_to_cm': 2.54,
    'cm_to_inches': 0.393701,
    'feet_to_m': 0.3048,
    'm_to_feet': 3.28084,
    'yards_to_m': 0.9144,
    'm_to_yards': 1.09361,
    'pounds_to_kg': 0.453592,
    'kg_to_pounds': 2.20462,
    'ounces_to_grams': 28.3495,
    'grams_to_ounces': 0.035274,
    'liters_to_gallons': 0.264172,
    'gallons_to_liters': 3.78541,
}

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
        if match_score < 80:
            return 'Please enter a valid city name.'
        
        response = requests.get(f'https://worldtimeapi.org/api/timezone/{best_match}')
        data = response.json()
        datetime_object = datetime.fromisoformat(data['datetime'])
        current_time = datetime_object.strftime('%I:%M %p')
        return f'The current time in {city.title()} is: {current_time}'
    except Exception as e:
        return 'An error occurred while fetching the time.'
    
# Google Translate API
def translate_text(text: str, source_language: str, target_language: str) -> tuple:
    try:
        translated = translator.translate(text, src=source_language, dest=target_language)
        return translated.text, translated.pronunciation
    except Exception as e:
        return f"An error occurred: {str(e)}", None,

# Unit Conversion
def convert_units(value: float, from_unit: str, to_unit: str, conversion_factors: dict) -> str:
    unit_mapping = {
        'fahrenheit': 'f', 
        'celsius': 'c', 
        'f': 'fahrenheit',
        'c': 'celsius',
        'miles': 'mi',
        'mi': 'miles',
        'kilometres': 'km',
        'km': 'kilometres',
        'inches': 'in',
        'in': 'inches',
        'cm': 'centimetres',
        'centimetres': 'cm',
        'feet': 'ft',
        'ft': 'feet',
        'yards': 'yd',
        'yd': 'yards',
        'm': 'metres',
        'metres': 'm',
        'kilograms': 'kg',
        'kg': 'kilograms',
        'pounds': 'lbs',
        'lbs': 'pounds',
        'ounces': 'oz',
        'oz': 'ounces',
        'grams': 'g',
        'g': 'grams',
        'liters': 'l',
        'l': 'liters',
        'litres': 'l',
        'gallons': 'gal',
        'gal': 'gallons'
    }
    from_unit = unit_mapping.get(from_unit.lower(), from_unit)
    to_unit = unit_mapping.get(to_unit.lower(), to_unit)
    
    conversion_key = f"{from_unit}_to_{to_unit}"
    conversion_key = conversion_key.replace("centimetres", "cm")
    conversion_key = conversion_key.replace("inches", "in")

    conversion_factor = conversion_factors.get(conversion_key)
    
    if conversion_factor is None:
        return f"No conversion factor found for {from_unit} to {to_unit}."
    converted_value = value * conversion_factor
    return f"{value} {from_unit} is {converted_value:.2f} {to_unit}" # .2f = 2 decimal places

# Roll a dice
def roll_dice() -> int:
    return random.randint(1,6)

# Flip a coin
def flip_coin() -> str:
    return random.choice(['heads', 'tails'])

# Response to an unsupported message
def choose_random_response(user_input: str) -> str:
    responses: Final[str] = [
        'I do not quite understand...',
        'What are you talking about?',
        'Do you mind rephrasing that?'
    ]
    return random.choice(responses) if user_input else 'You did not say anything...'

# Responses
def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()
    # no message
    if lowered == '':
        return 'Well, this is awkward...'
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
    # translate
    elif lowered.startswith('translate'):
        segments = lowered.split(' ', 4)
        if len(segments) < 4:
            return 'Please enter the text, source language and the target language.'
        text_to_translate = segments[1]
        source_language = segments[2]
        target_language = segments[3]
        translated_text, pronunciation = translate_text(text_to_translate, source_language, target_language)
        if pronunciation is not None:
            return f"Translated Text:\n{translated_text}\n\nPronunciation:\n{pronunciation}"
        else:
            return f"Translated Text:\n{translated_text}"
    # unit converter
    elif lowered.startswith('convert'):
        segments = lowered.split(' ')
        if len(segments) < 4:
            return 'Please enter the value and units to convert.'
        try:
            value = float(segments[1])
            from_unit = segments[2]
            to_unit = segments[3]
            result = convert_units(value, from_unit, to_unit, conversion_factors)
            return result
        except ValueError:
            return 'Invalid value for conversion. Please enter a numeric value.'
    # OTHER RESPONSES
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
    else:
        return choose_random_response(lowered)