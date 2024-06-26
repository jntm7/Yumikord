
# Unit Converter
async def convert_units_logic(value, from_unit, to_unit):
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
def calculator(user_input: str) -> str:
    tokens = user_input.split()
    try:
        num1 = float(tokens[0])
        operator = tokens[1]    
        num2 = float(tokens[2])

        if operator == '+':
            result = num1 + num2
        elif operator == '-':
            result = num1 - num2
        elif operator == '*':
            result = num1 * num2
        elif operator == '/':
            if num2 == 0: 
                return 'Division by zero is not possible.'
            result = num1 / num2
        else:
            return 'Please enter a valid operator: +, -, *, /.'

        return f'{result}'

    except ValueError:
        return 'Please enter valid numbers for calculation.'

def validate_expression(expression: str) -> bool:
    return any(char.isdigit() for char in expression) and any(char in expression for char in ['+', '-', '*', '/'])