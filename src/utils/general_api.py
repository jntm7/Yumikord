import requests
import aiohttp
from fuzzywuzzy import process
from datetime import datetime
from googletrans import Translator

# World Weather API
async def get_weather(city: str) -> str:
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

# World Time API
async def get_time(city):
    async with aiohttp.ClientSession() as session:
        try:
            # Fetch available timezones
            async with session.get('https://worldtimeapi.org/api/timezone') as timezones_response:
                timezones_response.raise_for_status()
                timezones = await timezones_response.json()

            # Find best match for the given city
            best_match, match_score = process.extractOne(city, timezones, scorer=process.fuzz.partial_ratio)
            if match_score < 80:
                return None, 'Please enter a valid city name.'

            # Fetch current time for the best match timezone
            async with session.get(f'https://worldtimeapi.org/api/timezone/{best_match}') as time_response:
                time_response.raise_for_status()
                data = await time_response.json()

            datetime_object = datetime.fromisoformat(data['datetime'])
            current_time = datetime_object.strftime('%I:%M %p')
            return best_match.replace("_", " ").title(), current_time
        except Exception as e:
            return None, f"Couldn't retrieve the time. Please try again later! ({e})"

# Translate (GoogleTrans Py Package)
translator = Translator()
def translate_text(text: str, source_language: str, target_language: str) -> tuple:
    try:
        translated = translator.translate(text, src=source_language, dest=target_language)
        return translated.text, translated.pronunciation
    except Exception as e:
        return f"An error occurred: {str(e)}", None,

# Dictionary API
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

# Exchange Rate API
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

# Currency Conversion API
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
    
# Cryptocurrency API
def get_crypto(id):
    try:
        response = requests.get(f"https://api.coincap.io/v2/assets/{id}")
        response.raise_for_status()
        data = response.json()
        asset_data = data['data']
        name = asset_data['name']
        symbol = asset_data['symbol']
        rank = asset_data['rank']
        supply = asset_data['supply']
        max_supply = asset_data['maxSupply']
        market_cap_usd = asset_data['marketCapUsd']
        price = asset_data['priceUsd']
        return f"Name: {name}\nSymbol: {symbol}\nRank: {rank}\nSupply: {supply}\nMax Supply: {max_supply}\nMarket Cap USD: ${market_cap_usd}\nPrice: ${price}"
    except Exception as e:
        return f"Couldn't fetch cryptocurrency data. Please try again later! {e}"

# Color Palette API
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

# Hacker News API
def get_hackernews() -> str:
    try:
        response = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json")
        response.raise_for_status()
        top_stories = response.json()

        if not top_stories:
            return "Couldn't retrieve any top stories from Hacker News right now. Please try again later!"

        id = top_stories[0]
        story_response = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{id}.json")
        story_response.raise_for_status()
        story_data = story_response.json()

        title = story_data.get('title', 'no title')
        url = story_data.get('url', 'no url')
        return f"Top Hacker News Story:\n {title}\n {url}"
    except Exception as e:
        return f"Couldn't retrieve any top stories from Hacker News right now. Please try again later! ({e})"
