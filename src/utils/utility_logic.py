import re
from typing import List, Union

# Unit Converter
async def convert_units(value, from_unit, to_unit):
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
    conversion_factor = conversion_factors.get(conversion_key)
    
    if conversion_factor is None:
        return f"No conversion factor found for {from_unit} to {to_unit}."
    converted_value = value * conversion_factor
    return f"{value} {from_unit} is {converted_value:.2f} {to_unit}"

# Calculator
def tokenize(expression: str) -> List[str]:
    return re.findall(r'\d+\.?\d*|\+|\-|\*|\/|\(|\)', expression)

def is_number(token: str) -> bool:
    try:
        float(token)
        return True
    except ValueError:
        return False

def apply_operator(operators: List[str], values: List[float], operator: str):
    right = values.pop()
    left = values.pop()
    if operator == '+':
        values.append(left + right)
    elif operator == '-':
        values.append(left - right)
    elif operator == '*':
        values.append(left * right)
    elif operator == '/':
        if right == 0:
            raise ValueError("Division by zero")
        values.append(left / right)

def calculate(tokens: List[str]) -> float:
    operators = []
    values = []
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}

    for token in tokens:
        if is_number(token):
            values.append(float(token))
        elif token == '(':
            operators.append(token)
        elif token == ')':
            while operators and operators[-1] != '(':
                apply_operator(operators, values, operators.pop())
            operators.pop()
        elif token in precedence:
            while operators and operators[-1] != '(' and precedence.get(operators[-1], 0) >= precedence[token]:
                apply_operator(operators, values, operators.pop())
            operators.append(token)

    while operators:
        apply_operator(operators, values, operators.pop())

    return values[0]

def calculator(expression: str) -> str:
    try:
        tokens = tokenize(expression)
        result = calculate(tokens)
        return f"The answer is: {result}"
    except ValueError as e:
        return str(e)
    except Exception as e:
        return f"An error occurred: {str(e)}"