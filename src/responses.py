from random import choice, randint
from typing import Final
from datetime import datetime, timedelta
from fuzzywuzzy import process
from googletrans import Translator
from urllib.parse import quote
import re

from utils.general import no_message_response
from commands.utility_commands import calculator_response
from utils.general_api import time_in_response, weather_response, hackernews_response, translate_response, dictionary_response, unit_conversion_response, exchange_rate_response, currency_conversion_response, crypto_price_response, color_palette_response, meme_response, joke_response, dadjoke_response, quote_response, fact_response, advice_response, affirmation_response, inspiration_response, yes_no_gif_response, pokemon_info_response, waifu_image_response
from utils.game_logic import play_rps_response, start_guesser_response, play_guesser_response
from commands.trivia_commands import trivia_game
from utils.game_logic import game_states
from utils.fun_api import hello_response, how_are_you_response, roll_dice_response, flip_coin_response, random_number_response


# Responses
def get_response(user_input: str, user_id: str = None) -> str:
    lowered: str = user_input.lower()

    # No Message
    if lowered == '':
        return no_message_response()

    # Calculator
    elif 'calculate' in lowered:
        expression = lowered.replace('calculate', '', 1).strip()
        return calculator_response(expression)

    # World Clock
    elif 'time in' in lowered:
         city = lowered.replace('time in', '', 1).strip()
         return time_in_response(city)
         
    # World Weather
    elif 'weather in' in lowered:
        city = lowered.replace('weather in', '', 1).strip()
        return weather_response(city)
        
    # Hacker News
    elif 'hackernews' in lowered:
        return hackernews_response()

    # Translate
    elif lowered.startswith('translate'):
        segments = lowered.split(' ', 4)
        if len(segments) < 4:
            return 'Please enter the text, source language and the target language.'
        text_to_translate = segments[1]
        source_language = segments[2]
        target_language = segments[3]
        return translate_response(text_to_translate, source_language, target_language)

    # Dictionary
    elif lowered.startswith('dictionary.'):
        word = lowered.split('.', 1)[1]
        return dictionary_response(word)

    # Unit Conversion
    elif lowered.startswith('convert'):
        segments = lowered.split(' ')
        if len(segments) < 4:
            return 'Please enter the value and units to convert.'
        try:
            value = float(segments[1])
            from_unit = segments[2]
            to_unit = segments[3]
            return unit_conversion_response(value, from_unit, to_unit)
        except ValueError:
            return 'Invalid value for conversion. Please enter a numeric value.'
    
    # Exchange Rate
    elif lowered.startswith('rate'):
        parts = lowered.split('.')
        if len(parts) == 3:
            from_currency = parts[1].upper()
            to_currency = parts[2].upper()
            return exchange_rate_response(from_currency, to_currency)
        else:
            return "Please provide the currencies in the format: rate.<currency>.<currency>."

    # Currency Conversion
    elif lowered.startswith('exchange'):
        parts = lowered.split('.')
        if len(parts) == 4:
            amount = float(parts[1])
            from_currency = parts[2].upper()
            to_currency = parts[3].upper()
            return currency_conversion_response(amount, from_currency, to_currency)
        else:
            return "Please provide the conversion in the format exchange.<amount>.<currency>.<currency>."

    # Cryptocurrency Price
    elif lowered.startswith('crypto'):
        parts = lowered.split('.')
        if len(parts) == 2:
            id = parts[1].lower()
            return crypto_price_response(id)
        else:
            return "Please provide the cryptocurrency symbol in the format crypto.<name>."

    # Color Palette
    elif 'color' in lowered:
        return color_palette_response()

    # Memes
    elif 'meme' in lowered:
        return meme_response()
    
    # Jokes
    elif 'joke' in lowered:
        return joke_response()
    
    elif 'dadjoke' in lowered:
        return dadjoke_response()
    
    # Quotes
    elif 'quote' in lowered:
        return quote_response()
    
    # Facts
    elif 'fact' in lowered:
        return fact_response()
    
    elif 'advice' in lowered:
        return advice_response()
    
    # Affirmation
    elif 'affirm' in lowered:
        return affirmation_response()

    # Inspiration
    elif 'inspire' in lowered:
        return inspiration_response()
    
    # Yes / No GIF
    elif 'yesno' in lowered:
        return yes_no_gif_response()
    
    # Pokemon Information
    elif lowered.startswith('pokemon.'):
        segments = lowered.split('.')
        if len(segments) < 2:
            return 'Please enter a valid Pokémon.'
        pokemon_name = segments[1].strip()
        return pokemon_info_response(pokemon_name)
    
    # Waifu Image
    elif lowered == 'waifu':
        return waifu_image_response()
    elif lowered == 'waifu.nsfw':
        return waifu_image_response(nsfw=True)

    # OTHER RESPONSES
    # Hello  
    elif 'hello' in lowered:
        return hello_response()
    
    # How are you
    elif 'how are you' in lowered:
        return how_are_you_response()
    
    # Roll Dice
    elif 'dice' in lowered:
        return roll_dice_response()
    
    # Flip Coin
    elif 'coin' in lowered:
        return flip_coin_response()
    
    # Random Number
    elif 'number' in lowered:
        return random_number_response()
    
    # Rock Paper Scissors
    elif lowered == 'play.rps':
        game_states[user_id] = {'active': True}
        return "Let's play Rock-Paper-Scissors! Type 'rock', 'paper', or 'scissors' to make your choice."

    elif user_id in game_states and game_states[user_id]['active'] and lowered in ['rock', 'paper', 'scissors']:
        return play_rps_response(user_id, lowered)
    
    # Number Guesser
    elif lowered == 'play.guess':
        return start_guesser_response(user_id)
    
    elif lowered.startswith('guess.'):
        guess = lowered.split('guess.', 1)[1].strip()
        return play_guesser_response(user_id, guess)

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

    def choose_random_response(command):
        responses = {
            "greet": ["Hello!", "Hi!", "Hey!"],
            "bye": ["Goodbye!", "See you!", "Bye!"]
        }
        return responses.get(command, ["I don't understand."])[0]

    command = "greet"

    return choose_random_response(command)