import requests
import random
import re
import html
from random import choice, randint
from typing import Final
from datetime import datetime, timedelta
from fuzzywuzzy import process
from googletrans import Translator
from urllib.parse import quote


# Response to an unsupported message
def choose_random_response(user_input: str) -> str:
    responses: Final[str] = [
        'Please refer to `?help` to learn more about what I can do.',
        'Please use `?help` to view all my supported commands.',
        'Please type `?help` to see all the supported features.',
    ]
    return random.choice(responses) if user_input else 'You did not say anything...'

# Responses
def get_response(user_input: str, user_id: str = None) -> str:
    lowered: str = user_input.lower()

    # No Message
    if lowered == '':
        return 'Well, this is awkward...'
    
    elif 'bug' in lowered:
        return 'For feature requests and bug reports, please review the [GitHub documentation](<https://github.com/jntm7/yumikord>). \nIf it is unable to be resolved, feel free to [open a new issue](<https://github.com/jntm7/Yumikord/issues>).\nPlease ensure the respective labels `enhancement` for feature requests and `bug` for issues are assigned.'

    # Calculator
    elif 'calculate' in lowered:
        expression = lowered.replace('calculate', '', 1).strip()
        if validate_expression(expression):
            return f'The answer is: {calculator(expression)}'
        else:
            return 'Please enter a valid calculation expression.'

    # World Clock
    elif 'time in' in lowered:
         city = lowered.replace('time in', '', 1).strip()
         if city:
            return get_current_time(city)
         else:
             return 'Please enter a valid city name.'
         
    # World Weather
    elif 'weather in' in lowered:
        city = lowered.replace('weather in', '', 1).strip()
        if city:
            return get_weather(city)
        else:
            return 'Please enter a valid city name.'
        
    # Hacker News
    elif 'hackernews' in lowered:
        return get_hackernews()

    # Translate
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

    # Dictionary
    elif lowered.startswith('dictionary.'):
        word = lowered.split('.', 1)[1]
        return get_dictionary(word)

    # Unit Conversion
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
    
    # Exchange Rate
    elif lowered.startswith('rate'):
        parts = lowered.split('.')
        if len(parts) == 3:
            from_currency = parts[1].upper()
            to_currency = parts[2].upper()
            return get_exchange_rate(from_currency, to_currency)
        else:
            return "Please provide the currencies in the format: rate.<currency>.<currency>."

    # Currency Conversion
    elif lowered.startswith('exchange'):
        parts = lowered.split('.')
        if len(parts) == 4:
            amount = float(parts[1])
            from_currency = parts[2].upper()
            to_currency = parts[3].upper()
            return convert_currency(amount, from_currency, to_currency)
        else:
            return "Please provide the conversion in the format exchange.<amount>.<currency>.<currency>."

    # Cryptocurrency Price
    elif lowered.startswith('crypto'):
        parts = lowered.split('.')
        if len(parts) == 2:
            id = parts[1].lower()
            price_info = get_crypto(id)
            return price_info
        else:
            return "Please provide the cryptocurrency symbol in the format crypto.<name>."

    # Color Palette
    elif 'color' in lowered:
        return get_color_palette()

    # Memes
    elif 'meme' in lowered:
        return get_meme()
    
    # Jokes
    elif 'joke' in lowered:
        return get_joke()
    
    elif 'dadjoke' in lowered:
        return get_dadjoke()
    
    # Quotes
    elif 'quote' in lowered:
        return get_quote()
    
    # Facts
    elif 'fact' in lowered:
        return get_fact()
    
    elif 'advice' in lowered:
        return get_advice()
    
    # Affirmation
    elif 'affirm' in lowered:
        return get_affirmation()

    # Inspiration
    elif 'inspire' in lowered:
        return get_inspiration()
    
    # Yes / No GIF
    elif 'yesno' in lowered:
        return get_yes_no_gif()
    
    # Pokemon Information
    elif lowered.startswith('pokemon.'):
        segments = lowered.split('.')
        if len(segments) < 2:
            return 'Please enter a valid Pokémon.'
        pokemon_name = segments[1].strip()
        return get_pokemon_info(pokemon_name)
    
    # Waifu Image
    elif lowered == 'waifu':
        return get_waifu_image()
    elif lowered == 'waifu.nsfw':
        return get_waifu_image(nsfw=True)

    # OTHER RESPONSES
    # Hello  
    elif 'hello' in lowered:
        return 'Hello there!'
    
    # How are you
    elif 'how are you' in lowered:
        return 'Great, thanks!'
    
    # Roll Dice
    elif 'dice' in lowered:
        return f'You rolled: {roll_dice()}'
    
    # Flip Coin
    elif 'coin' in lowered:
        return f'You got: {flip_coin()}'
    
    # Random Number
    elif 'number' in lowered:
        return f'You got: {random_number()}'
    
    # Rock Paper Scissors
    elif lowered == 'play.rps':
        active_rps[user_id] = True
        return "Let's play Rock-Paper-Scissors! Type 'rock', 'paper', or 'scissors' to make your choice."
    
    elif user_id in active_rps and lowered in ['rock', 'paper', 'scissors']:
        return play_rps(user_id, lowered)
    
    # Number Guesser
    elif lowered == 'play.guess':
        return start_guesser(user_id)
    
    elif lowered.startswith('guess.'):
        guess = lowered.split('guess.', 1)[1].strip()
        return play_guesser(user_id, guess)

    # Trivia
    elif lowered.startswith("play.trivia"):
        if not trivia_game.active_game:
            question, options = trivia_game.start_game()
            if question:
                return f"[Question] {question}\n[Options]\n" + "\n".join([f"{i+1}. {answer}" for i, answer in enumerate(options)])
            else:
                return f"Couldn't fetch any trivia questions. Please try again later!"
        else:
            match = re.match(r"^play\.trivia\s+(\d+)$", lowered)
            if match:
                answer_index = int(match.group(1)) - 1
                answered, response = trivia_game.answer_question(answer_index)
                if answered:
                    return response
                else:
                    return response
            else:
                return "Invalid format. Please use `play.trivia <number>` to answer the question."

    else:
        return choose_random_response(user_input)