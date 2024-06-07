import random
from random import choice, randint
from typing import Final
import requests
from datetime import datetime
from fuzzywuzzy import process
from googletrans import Translator
from urllib.parse import quote

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

        if isinstance(num1, int) and isinstance(num2, int): 
            return f'{int(result)}'
        else:
            return f'{result}'

    except ValueError:
        return 'Please enter valid numbers for calculation.'

def validate_expression(expression: str) -> bool:
    return any(char.isdigit() for char in expression) and any(char in expression for char in ['+', '-', '*', '/'])

# World Time
def get_current_time(city):
    try:
        timezones_response = requests.get('https://worldtimeapi.org/api/timezone')
        timezones_response.raise_for_status()
        timezones = timezones_response.json()

        best_match, match_score = process.extractOne(city, timezones, scorer = process.fuzz.partial_ratio)
        if match_score < 80:
            return 'Please enter a valid city name.'
        
        time_response = requests.get(f'https://worldtimeapi.org/api/timezone/{best_match}')
        time_response.raise_for_status()
        data = time_response.json()
        datetime_object = datetime.fromisoformat(data['datetime'])
        current_time = datetime_object.strftime('%I:%M %p')
        return f'The current time in {best_match.replace("_", " ").title()} is: {current_time}'
    except Exception as e:
        return f"Couldn't retrieve the time for {city}. Please try again later! ({e})"

# World Weather
def get_weather(city: str) -> str:
    try:
        cities_response = requests.get('https://raw.githubusercontent.com/lutangar/cities.json/master/cities.json')
        cities_response.raise_for_status()
        cities = cities_response.json()
        city_names = [c['name'] for c in cities]

        exact_matches = [name for name in city_names if name.lower() == city.lower()]
        if exact_matches:
            best_match = exact_matches[0]
        else:
            startswith_matches = [name for name in city_names if name.lower().startswith(city.lower())]
            if startswith_matches:
                best_match = startswith_matches[0]
            else:
                best_match, match_score = process.extractOne(city, city_names, scorer=process.fuzz.partial_ratio)
                if match_score < 80:
                    return 'Please enter a valid city name.'
        
        city_encoded = best_match.replace(' ', '+')
        weather_response = requests.get(f'https://wttr.in/{city_encoded}?format=%C+%t')
        weather_response.raise_for_status()
        weather_data = weather_response.text.strip()
        return f"The weather in {best_match.title()} is: {weather_data}"
    except Exception as e:
        return f"Couldn't retrieve the weather for {city}. Please try again later! ({e})"

# Translate
translator = Translator()
def translate_text(text: str, source_language: str, target_language: str) -> tuple:
    try:
        translated = translator.translate(text, src=source_language, dest=target_language)
        return translated.text, translated.pronunciation
    except Exception as e:
        return f"An error occurred: {str(e)}", None,

# Dictionary
def get_dictionary(word: str) -> str:
    try:
        response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
        response.raise_for_status()
        data = response.json()

        if isinstance(data, list):
            definitions = data[0].get('meanings', [])
            if not definitions:
                return f"No definitions found for the word: {word}"
            
            definition_text = f"Definitions for '{word}':\n"
            for meaning in definitions:
                part_of_speech = meaning.get('partOfSpeech', 'Unknown')
                definitions_list = meaning.get('definitions', [])
                
                for i, definition in enumerate(definitions_list, start=1):
                    definition_text += f"{i}. ({part_of_speech}) {definition.get('definition')}\n"

            return definition_text.strip()
        else:
            return f"Couldn't find the word '{word}'. Please check the spelling and try again."
    except Exception as e:
        return f"Couldn't retrieve any dictionary information. Please try again later! ({e})"

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
    return f"{value} {from_unit} is {converted_value:.2f} {to_unit}"

# Exchange Rate
def get_exchange_rate(from_currency: str, to_currency: str) -> str:
    try:
        response = requests.get(f"https://api.frankfurter.app/latest?from={from_currency}&to={to_currency}")
        response.raise_for_status()
        data = response.json()
        rate = data['rates'].get(to_currency)
        if rate:
            return f"The exchange rate from {from_currency} to {to_currency} is {rate}."
        else:
            return f"Currency {from_currency} not found. Please enter a valid currency."
    except Exception as e:
        return "Couldn't retrieve exchange rate information. Please try again later! ({e})"

# Currency Conversion
def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
    try:
        response = requests.get(f"https://api.frankfurter.app/latest?amount={amount}&from={from_currency}&to={to_currency}")
        response.raise_for_status()
        data = response.json()
        converted_amount = data['rates'].get(to_currency)
        if converted_amount:
            return f"{amount} {from_currency} is {converted_amount:.2f} {to_currency}."
        else:
            return f"Currency {to_currency} not found."
    except Exception as e:
        return f"Couldn't retrieve conversion rate. Please try again later! ({e})"

# Color Palette
def get_color_palette() -> str:
    try:
        data = {"model": "default"}
        response = requests.post("http://colormind.io/api/", json=data)
        response.raise_for_status()
        color_data = response.json()
        color_palette = color_data.get("result")
        
        if not color_palette:
            return "There was no color palette received from the API. Please try again later!"
        color_text = "Generated Color Palette:\n"
        for color in color_palette:
            color_text += f"RGB: {color}\n"
        return color_text
    except Exception as e:
        return f"Couldn't retrieve any color palettes right now. Please try again later! ({e})"

# Memes API
def get_meme() -> str:
    try:
        response = requests.get("https://meme-api.com/gimme")
        response.raise_for_status()
        meme = response.json()
        return meme["url"]
    except Exception as e:
        return f"Couldn't retrieve any memes right now. Please try again later! ({e})"

# Jokes API
def get_joke() -> str:
    try:
        response = requests.get("https://v2.jokeapi.dev/joke/Any")
        response.raise_for_status()
        joke = response.json()
        if joke['type'] == 'single':
            return joke['joke']
        else:
            return f"{joke['setup']}\n{joke['delivery']}"
    except Exception as e:
        return f"Couldn't retrieve any jokes right now. Please try again later! ({e})"

# Quotes API
def get_quote() -> str:
    try:
        response = requests.get("https://zenquotes.io/api/random")
        response.raise_for_status()
        quote = response.json()[0]
        return f'"{quote["q"]}"\n— {quote["a"]}'
    except Exception as e:
        return f"Couldn't retrieve any quotes right now. Please try again later! ({e})" 

# Facts API
def get_fact() -> str:
    try:
        response = requests.get("https://uselessfacts.jsph.pl/random.json?language=en")
        response.raise_for_status()
        fact_data = response.json()
        fact_text = fact_data.get('text', 'No fact available')
        return f"{fact_text}"
    except Exception as e:
        return f"Couldn't retrieve any facts right now. Please try again later! ({e})"

# Reddit Subreddit Fetcher
def get_subreddit_posts(subreddit, limit=3):
    try:
        response = requests.get("https://api.pushshift.io/reddit/search/submission/?subreddit={subreddit}&limit={limit}")
        response.raise_for_status()
        posts = response.json()['data']
        if posts:
            return formatted_posts(posts)
        else:
            return "No posts found in the subreddit."
    except Exception as e:
        return f"Couldn't retrieve any posts from r/{subreddit} right now. Please try again later! ({e})"

def formatted_posts(posts: list) -> str:
    formatted = ""
    for post in posts:
        formatted += f"Title: {post['title']}\n"
        formatted += f"Author: {post['author']}\n"
        formatted += f"URL: {post['url']}\n"
    return formatted

# Pokemon API
def get_pokemon_info(pokemon_name):
    try:
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}")
        response.raise_for_status()
        pokemon_data = response.json()
        if pokemon_data:
            name = pokemon_data['name'].capitalize()
            types = ', '.join([t['type']['name'].capitalize() for t in pokemon_data['types']])
            abilities = ', '.join([a['ability']['name'].capitalize() for a in pokemon_data['abilities']])
            stats = ', '.join([f"{s['stat']['name'].capitalize()}: {s['base_stat']}" for s in pokemon_data['stats']])
            sprite_url = pokemon_data['sprites']['front_default']
            return f"**Name:** {name}\n**Type(s):** {types}\n**Abilities:** {abilities}\n**Base Stats:** {stats}\n**Sprite:** {sprite_url}"
        else:
            return f"Please enter a valid Pokémon."
    except Exception as e:
        return f"Couldn't retrieve anything from PokéAPI. Please try again later! ({e})"

# Waifu Image
def get_waifu_image(nsfw: bool = False) -> str:
    sfw_tags = ["waifu", "maid", "selfies", "uniform"]
    nsfw_tags = ["ero", "ass", "hentai", "milf", "oral", "paizuri", "ecchi", "oppai"]
    try:
        if nsfw:
            tag = random.choice(nsfw_tags)
            response = requests.get(f"https://api.waifu.im/search?included_tags={tag}")
        else:
            tag = random.choice(sfw_tags)
            response = requests.get(f"https://api.waifu.im/search?included_tags={tag}")
        response.raise_for_status()
        waifu_data = response.json()
        if waifu_data and 'images' in waifu_data and len(waifu_data['images']) > 0:
            image_url = waifu_data['images'][0]['url']
            return image_url
        else:
            return "Couldn't retrieve any waifu images right now. Please try again later!"
    except Exception as e:
        return f"Couldn't retrieve any waifu images right now. Please try again later! ({e})"

# Anime Facts
def get_anime_fact() -> str:
    try:
        anime_list_url = "https://anime-facts-rest-api.herokuapp.com/api/v1"
        response = requests.get(anime_list_url)
        response.raise_for_status()
        anime_list = response.json().get('data', [])

        if anime_list:
            random_anime = random.choice(anime_list)
            anime_name = random_anime['anime_name']

            anime_facts_url = f"https://anime-facts-rest-api.herokuapp.com/api/v1/:{anime_name}"
            response = requests.get(anime_facts_url)
            response.raise_for_status()
            anime_facts = response.json().get('data', [])

            if anime_facts:
                random_fact = random.choice(anime_facts)
                return random_fact['fact']
            else:
                return "Couldn't retrieve any facts for this anime."
        else:
            return "Couldn't retrieve this anime."
    except Exception as e:
        return f"Couldn't retrieve any anime facts right now. Please try again later! ({e})"

# Cat GIFs
def get_cat() -> str:
    try:
        response = requests.get("https://www.cataas.com/cat?json=true")
        response.raise_for_status()
        cat_data = response.json()
        if cat_data and 'url' in cat_data:
            gif_url = f"https://cataas.com{cat_data['url']}"
            return gif_url
        else:
            return "Couldn't retrieve any cats right now. Please try again later!"
    except Exception as e:
        return f"Couldn't retrieve any cats right now. Please try again later! ({e})"

# Roll a dice
def roll_dice() -> int:
    return random.randint(1,6)

# Flip a coin
def flip_coin() -> str:
    return random.choice(['heads', 'tails'])

# Random Number Generator
def random_number(command: str) -> str:
    try:
        _, min_val, max_val = command.split()
        min_val = int(min_val)
        max_val = int(max_val)
        return f'Your random number is {random.randint(min_val, max_val)}'
    except ValueError:
        return 'Please provide valid numbers for the range.'

# Rock Paper Scissors
active_rps = {}

def play_rps(user_id, user_choice):
    choices = ['rock', 'paper', 'scissors']
    bot_choice = random.choice(choices)
    active_rps.pop(user_id, None)

    if user_choice not in choices:
        return "Please choose one of: rock, paper or scissors."
    
    if user_choice == bot_choice:
        return f"Both chose {user_choice}. It's a draw!"
    elif (user_choice == 'rock' and bot_choice == 'scissors') or \
         (user_choice == 'paper' and bot_choice == 'rock') or \
         (user_choice == 'scissors' and bot_choice == 'paper'):
        return f"You chose {user_choice} and I chose {bot_choice}. You win, congratulations!"
    else:
        return f"You chose {user_choice} and I chose {bot_choice}. You lose, better luck next time!"

# Number Guesser
game_states = {}

def start_guesser(user_id):
    secret_number = random.randint(1,100)
    attempts = 0
    max_attempts = 8
    game_states[user_id] = {'number': secret_number, 'attempts': attempts}
    return f"I've chosen a number between 1 and 100. Can you guess it? I'll give you {max_attempts} chances. Let's start!\n"

def play_guesser(user_id, guess):
    if user_id not in game_states:
        return "To start a game, please enter 'play.guess'."
    
    game_state = game_states[user_id]
    secret_number = game_state['number']
    attempts = game_state['attempts'] + 1
    max_attempts = 8
    response = ""

    try:
        guess = int(guess)
        if guess < secret_number:
            response += f"Too low! Guess higher. You have {max_attempts - attempts} attempts left.\n"
        elif guess > secret_number:
            response += f"Too high! Guess lower. You have {max_attempts - attempts} attempts left.\n"
        else:
            response += f"Congratulations! You guessed the number {secret_number} in {attempts} attempts, very impressive!\n"
            del game_states[user_id]
            return response
    except ValueError:
        response += "Please enter a valid number.\n"
        return response

    if  attempts >= max_attempts:
        response += f"Unfortunately, you've run out of attempts. The number I chose was {secret_number}. Better luck next time!\n"
        del game_states[user_id]
    else:
        game_state['attempts'] = attempts
        game_states[user_id] = game_state

    return response

# Response to an unsupported message
def choose_random_response(user_input: str) -> str:
    responses: Final[str] = [
        'I do not quite understand...',
        'What are you talking about?',
        'Do you mind rephrasing that?',
        'Stop yapping nonsense.',
        'Type "help" to learn more about what I can do.'
    ]
    return random.choice(responses) if user_input else 'You did not say anything...'

# Responses
def get_response(user_input: str, user_id: str = None) -> str:
    lowered: str = user_input.lower()

    # No Message
    if lowered == '':
        return 'Well, this is awkward...'
    
    # Help
    elif lowered == 'help':
            help_text = """
            **Here are my supported commands:**

            `calculate <expression>` - Calculates the given mathematical expression.
            `convert <value> <from_unit> <to_unit>` - Converts a value from one unit to another.
            `rate.<from_currency>.<to_currency>` - Fetches the exchange rate between two currencies.
            `exchange.<amount>.<from_currency>.<to_currency>` - Converts an amount in one currency to another.
            
            `time in <city>` - Displays the current time in the specified city.
            `weather in <city>` - Displays the current weather in the specified city.

            `translate <text> <source_language> <target_language>` - Translates text from one language to another.
            `dictionary.<word>` - Defines a word.
            `color` - Generates a random color palette.
            
            `?play <link>` - start audio playback from a specified link
            `?pause` - pause audio playback
            `?resume` - resume audio playback
            `?stop` - stop audio playback
            `?loop` - loop audio playback
            `?endloop` - stop looping audio playback

            `dice` - Rolls a 6-sided dice.
            `coin` - Flips a 2-sided coin.
            `number <min> <max>` - Generates a random number between a specified range.
            `play.rps` - Play a game of rock-paper-scissors.
            `play.guess` - Play a game of number guessing.
            `guess.<number>` - Input after starting the number guessing game.

            `joke` - Tells you a random joke.
            `fact` - Tells you a random fact.
            `meme` - Fetches a random meme.
            `quote` - Fetches a random quote.
            `cat` - Fetches a random cat image.
            
            `waifu` - Fetches a random SFW waifu image.
            `waifu.nsfw` - Fetches a random NSFW waifu image.
            `animefact` - Provides a random anime fact.
            `pokemon.<pokemon_name>` - Provides information about the specified Pokémon.
            `subreddit.<subreddit_name>` - Fetches posts from the specified subreddit.
            """
            return help_text

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

    # Color Palette
    elif 'color' in lowered:
        return get_color_palette()

    # Memes
    elif 'meme' in lowered:
        return get_meme()
    
    # Jokes
    elif 'joke' in lowered:
        return get_joke()
    
    # Quotes
    elif 'quote' in lowered:
        return get_quote()
    
    # Facts
    elif 'fact' in lowered:
        return get_fact()
    
    # Reddit Subreddit Fetcher
    elif lowered.startswith('subreddit.'):
        subreddit = lowered.split('.')[1].strip()
        if len(subreddit) < 1:
            return 'Please enter a valid subreddit.'
        return get_subreddit_posts(subreddit)
    
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
    
    # Anime Facts
    elif 'anime' in lowered:
        return get_anime_fact()
    
    # Cat Images
    elif 'cat' in lowered:
        return get_cat()
    
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

    else:
        return choose_random_response(lowered)
