import random
from random import choice, randint
from typing import Final
import requests
from datetime import datetime
from fuzzywuzzy import process
from googletrans import Translator
from urllib.parse import quote
import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
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

# World Weather API

cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

def get_weather(city: str) -> str:
    try:
        latitude, longitude = get_lat_lon(city)
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "hourly": "temperature_2m"
        }
        responses = openmeteo.weather_api(url, params=params)
        response = responses[0]
        coordinates = f"{response.Latitude()}°N {response.Longitude()}°E"
        elevation = f"Elevation {response.Elevation()} m asl"
        timezone = f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}"
        utc_offset = f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s"
        hourly = response.Hourly()
        hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
        hourly_data = {
            "date": pd.date_range(
                start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
                end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
                freq=pd.Timedelta(seconds=hourly.Interval()),
                inclusive="left"
            )
        }
        hourly_data["temperature_2m"] = hourly_temperature_2m
        hourly_dataframe = pd.DataFrame(data=hourly_data)
        weather_info = f"Coordinates: {coordinates}\n{elevation}\n{timezone}\n{utc_offset}\n\nHourly Data:\n{hourly_dataframe}"
        return weather_info
    except Exception as e:
        return f"Couldn't retrieve weather information for {city}. ({e})"
    
def get_lat_lon(city: str):
    city_coordinates = {
        "hong kong": (22.3193, 114.1694),
    }
    return city_coordinates.get(city.lower(), (None, None))

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
def get_jokeapi_joke() -> str:
    try:
        response = requests.get("https://v2.jokeapi.dev/joke/Any")
        response.raise_for_status()
        joke = response.json()
        if joke['type'] == 'single':
            return joke['joke']
        else:
            return f"{joke['setup']}{joke['delivery']}"
    except Exception as e:
        return f"Couldn't retrieve any jokes right now. Please try again later! ({e})"

# Quotes API
def get_quote() -> str:
    try:
        response = requests.get("https://zenquotes.io/api/random")
        response.raise_for_status()
        quote = response.json()[0]
        return f"{quote['q']}\n— {quote['a']}"
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

# Response to an unsupported message
def choose_random_response(user_input: str) -> str:
    responses: Final[str] = [
        'I do not quite understand...',
        'What are you talking about?',
        'Do you mind rephrasing that?'
        'Stop yapping nonsense.'
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
         
    # world weather information
    elif 'weather in' in lowered:
        city = lowered.replace('weather in', '', 1).strip()
        if city:
            return get_weather(city)
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
    
    # memes
    elif 'meme' in lowered:
        return get_meme()
    
    # jokes
    elif 'joke' in lowered:
        return get_jokeapi_joke()
    
    # quotes
    elif 'quote' in lowered:
        return get_quote()
    
    # facts
    elif 'fact' in lowered:
        return get_fact()
    
    # reddit subreddit fetcher
    elif lowered.startswith('subreddit.'):
        subreddit = lowered.split('.')[1].strip()
        if len(subreddit) < 1:
            return 'Please enter a valid subreddit.'
        return get_subreddit_posts(subreddit)
    
    # pokemon information
    elif lowered.startswith('pokemon.'):
        segments = lowered.split('.')
        if len(segments) < 2:
            return 'Please enter a valid Pokémon.'
        pokemon_name = segments[1].strip()
        return get_pokemon_info(pokemon_name)
    
    # waifu image
    elif lowered == 'waifu':
        return get_waifu_image()
    elif lowered == 'waifu.nsfw':
        return get_waifu_image(nsfw=True)
    
    # anime facts
    elif 'anime' in lowered:
        return get_anime_fact()
    
    # cat gifs
    elif 'cat' in lowered:
        return get_cat()
    
    # OTHER RESPONSES
    # hello  
    elif 'hello' in lowered:
        return 'Hello there!'
    
    # how are you
    elif 'how are you' in lowered:
        return 'Great, thanks!'
    
    # roll dice
    elif 'dice' in lowered:
        return f'You rolled: {roll_dice()}'
    
    # flip coin
    elif 'coin' in lowered:
        return f'You got: {flip_coin()}'
    
    else:
        return choose_random_response(lowered)
