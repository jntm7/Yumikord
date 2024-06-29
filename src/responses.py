from random import choice, randint
from typing import Final
from datetime import datetime, timedelta
from fuzzywuzzy import process
from googletrans import Translator
from urllib.parse import quote

# Import Called Functions
from commands.help_commands import get_help
from utils.general import choose_random_response, no_message_response, bug_response
from utils.utility_logic import convert_units, calculator
from utils.general_api import get_time, get_weather, translate_text, get_dictionary, get_exchange_rate, convert_currency, get_crypto, get_color_palette, get_hackernews
from utils.fun_api import get_meme, get_joke, get_dadjoke, get_quote, get_fact, get_advice, get_affirmation, get_inspiration, get_yes_no_gif, get_pokemon_info, get_waifu_image
from utils.game_logic import game_states, roll_dice, flip_coin, generate_random_number, play_rps, start_guesser, play_guesser
from commands.trivia_commands import handle_trivia_command

# Get Responses
async def get_response(user_input: str, channel, user_id: str = None) -> str:
    lowered: str = user_input.lower()

    # No Message
    if lowered == '':
        return no_message_response()

    # Help
    elif 'help' in lowered:
        return await get_help(channel)

    # Bug Response
    elif 'bug' in lowered:
        return bug_response()

    # Calculator
    elif 'calculate' in lowered:
        expression = lowered.replace('calculate', '', 1).strip()
        return calculator(expression)

    # World Clock
    elif 'time in' in lowered:
         city = lowered.replace('time in', '', 1).strip()
         return await get_time(city)
         
    # World Weather
    elif 'weather in' in lowered:
        city = lowered.replace('weather in', '', 1).strip()
        return await get_weather(city)
        
    # Hacker News
    elif 'hackernews' in lowered:
        return await get_hackernews()

    # Translate
    elif lowered.startswith('translate'):
        segments = lowered.split(' ', 4)
        if len(segments) < 4:
            return 'Please enter the text, source language and the target language.'
        text_to_translate = segments[1]
        source_language = segments[2]
        target_language = segments[3]
        return await translate_text(text_to_translate, source_language, target_language)

    # Dictionary
    elif lowered.startswith('dictionary.'):
        word = lowered.split('.', 1)[1]
        return await get_dictionary(word)

    # Unit Conversion
    elif lowered.startswith('convert'):
        segments = lowered.split(' ')
        if len(segments) < 4:
            return 'Please enter the value and units to convert.'
        try:
            value = float(segments[1])
            from_unit = segments[2]
            to_unit = segments[3]
            return await convert_units(value, from_unit, to_unit)
        except ValueError:
            return 'Invalid value for conversion. Please enter a numeric value.'
    
    # Exchange Rate
    elif lowered.startswith('rate'):
        parts = lowered.split('.')
        if len(parts) == 3:
            from_currency = parts[1].upper()
            to_currency = parts[2].upper()
            return await get_exchange_rate(from_currency, to_currency)
        else:
            return "Please provide the currencies in the format: rate.<currency>.<currency>."

    # Currency Conversion
    elif lowered.startswith('exchange'):
        parts = lowered.split('.')
        if len(parts) == 4:
            amount = float(parts[1])
            from_currency = parts[2].upper()
            to_currency = parts[3].upper()
            return await convert_currency(amount, from_currency, to_currency)
        else:
            return "Please provide the conversion in the format exchange.<amount>.<currency>.<currency>."

    # Cryptocurrency Price
    elif lowered.startswith('crypto'):
        parts = lowered.split('.')
        if len(parts) == 2:
            id = parts[1].lower()
            return await get_crypto(id)
        else:
            return "Please provide the cryptocurrency symbol in the format crypto.<name>."

    # Color Palette
    elif 'color' in lowered:
        return await get_color_palette()

    # Memes
    elif 'meme' in lowered:
        return await get_meme()
    
    # Jokes
    elif 'joke' in lowered:
        return await get_joke()
    
    elif 'dadjoke' in lowered:
        return await get_dadjoke()
    
    # Quotes
    elif 'quote' in lowered:
        return await get_quote()
    
    # Facts
    elif 'fact' in lowered:
        return await get_fact()
    
    elif 'advice' in lowered:
        return await get_advice()
    
    # Affirmation
    elif 'affirm' in lowered:
        return await get_affirmation()

    # Inspiration
    elif 'inspire' in lowered:
        return await get_inspiration()
    
    # Yes / No GIF
    elif 'yesno' in lowered:
        return await get_yes_no_gif()
    
    # Pokemon Information
    elif lowered.startswith('pokemon.'):
        segments = lowered.split('.')
        if len(segments) < 2:
            return 'Please enter a valid Pokémon.'
        pokemon_name = segments[1].strip()
        return await get_pokemon_info(pokemon_name)
    
    # Waifu Image
    elif lowered == 'waifu':
        return get_waifu_image()
    elif lowered == 'waifu.nsfw':
        return get_waifu_image(nsfw=True)

    # OTHER RESPONSES
    # Hello  
    elif 'hello' in lowered:
        return "Hello! How can I help you today?"
    
    # How are you
    elif 'how are you' in lowered:
        return "I'm doing amazing! Hope you are having a fantastic day too!"
    
    # Roll Dice
    elif 'dice' in lowered:
        return roll_dice()
    
    # Flip Coin
    elif 'coin' in lowered:
        return flip_coin()
    
    # Random Number
    elif 'number' in lowered:
        parts = lowered.split()
        number_index = parts.index('number') if 'number' in parts else -1
        if number_index != -1 and number_index + 1 < len(parts):
            try:
                min_val = int(parts[number_index + 1])
                max_val = int(parts[number_index + 2]) if number_index + 2 < len(parts) else 100
                return generate_random_number(min_val, max_val)
            except ValueError:
                return "Please enter valid numbers for the range."
        else:
            return generate_random_number(1, 100)
    
    # Rock Paper Scissors
    elif lowered == 'play.rps':
        game_states[user_id] = {'active': True}
        return "Let's play Rock-Paper-Scissors! Type 'rock', 'paper', or 'scissors' to make your choice."

    elif user_id in game_states and game_states[user_id]['active'] and lowered in ['rock', 'paper', 'scissors']:
        return play_rps(user_id, lowered)
    
    # Number Guesser
    elif lowered == 'play.guess':
        return start_guesser(user_id)
    
    elif lowered.startswith('guess.'):
        guess = lowered.split('guess.', 1)[1].strip()
        return play_guesser(user_id, guess)

    # Trivia
    elif lowered.startswith("play.trivia"):
        response = await handle_trivia_command(lowered)
        return response
    
    return choose_random_response(lowered)