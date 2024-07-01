import aiohttp
import json
import random

# Memes API
async def get_meme() -> str:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://meme-api.com/gimme") as response:
                response.raise_for_status()
                meme = await response.json()
                return meme["url"]
    except Exception as e:
        return f"Couldn't retrieve any memes right now. Please try again later! ({e})"

# Jokes API
async def get_joke() -> str:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://v2.jokeapi.dev/joke/Any") as response:
                response.raise_for_status()
                joke = await response.json()
                if joke['type'] == 'single':
                    return joke['joke']
                else:
                    return f"{joke['setup']}\n{joke['delivery']}"
    except Exception as e:
        return f"Couldn't retrieve any jokes right now. Please try again later! ({e})"

# Dad Jokes API
async def get_dadjoke() -> str:
    try:
        headers = {'Accept': 'application/json'}
        async with aiohttp.ClientSession() as session:
            async with session.get("https://icanhazdadjoke.com", headers=headers) as response:
                response.raise_for_status()
                data = await response.json()
                return data['joke']
    except Exception as e:
        return f"Couldn't retrieve any dad jokes right now. Please try again later! ({e})"

# Quotes API
async def get_quote() -> str:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://zenquotes.io/api/random") as response:
                response.raise_for_status()
                quote = await response.json()
                quote = quote[0]
                return f'"{quote["q"]}"\n— {quote["a"]}'
    except Exception as e:
        return f"Couldn't retrieve any quotes right now. Please try again later! ({e})"

# Facts API
async def get_fact() -> str:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://uselessfacts.jsph.pl/random.json?language=en") as response:
                response.raise_for_status()
                fact_data = await response.json()
                fact_text = fact_data.get('text', 'No fact available')
                return f"{fact_text}"
    except Exception as e:
        return f"Couldn't retrieve any facts right now. Please try again later! ({e})"

# Advice API
async def get_advice() -> str:
    headers = {"Accept": "application/json"}
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get("https://api.adviceslip.com/advice") as response:
                response.raise_for_status()
                text_response = await response.text()
                try:
                    data = json.loads(text_response)
                    advice = data['slip']['advice']
                    return f"Here's some advice: {advice}"
                except json.JSONDecodeError:
                    return f"The response was not in valid JSON format. Response: {text_response}"
                except KeyError:
                    return f"The response didn't contain the expected data. Response: {text_response}"
    except aiohttp.ClientError as e:
        return f"Couldn't retrieve any advice right now. Please try again later! ({e})"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

# Affirmations API
async def get_affirmation() -> str:
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get("https://affirmations.dev") as response:
                response.raise_for_status()
                data = await response.json()
                affirmation = data['affirmation']
                return affirmation
    except Exception as e:
        return f"Couldn't retrieve any affirmations right now. Please try again later! ({e})"

# Inspiration API
async def get_inspiration() -> str:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.fisenko.net/v1/quotes/en/random") as response:
                response.raise_for_status()
                data = await response.json()
                inspiration = f'"{data["text"]}"\n— {data["author"]["name"]}'
                return inspiration
    except Exception as e:
        return f"Couldn't retrieve any inspiration right now. Please try again later! ({e})"

# Yes/No GIF API
async def get_yes_no_gif() -> str:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://yesno.wtf/api") as response:
                response.raise_for_status()
                data = await response.json()
                yesno = data['image']
                return yesno
    except Exception as e:
        return f"Couldn't retrieve any yes/no GIFs right now. Please try again later! ({e})"

# Pokemon API
async def get_pokemon_info(pokemon_name):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}") as response:
                response.raise_for_status()
                pokemon_data = await response.json()
                if pokemon_data:
                    name = pokemon_data['name'].capitalize()
                    types = ', '.join([t['type']['name'].capitalize() for t in pokemon_data['types']])
                    abilities = ', '.join([a['ability']['name'].capitalize() for a in pokemon_data['abilities']])
                    stats = ', '.join([f"{s['stat']['name'].capitalize()}: {s['base_stat']}" for s in pokemon_data['stats']])
                    sprite_url = pokemon_data['sprites']['front_default']
                    return f"**Name:** {name}\n**Type(s):** {types}\n**Abilities:** {abilities}\n**Base Stats:** {stats}\n**Sprite:** {sprite_url}"
                else:
                    return "Please enter a valid Pokémon."
    except Exception as e:
        return f"Couldn't retrieve anything from PokéAPI. Please try again later! ({e})"

# Waifu Image
async def get_waifu_image(nsfw: bool = False) -> str:
    sfw_tags = ["waifu", "maid", "selfies", "uniform"]
    nsfw_tags = ["ero", "ass", "hentai", "milf", "oral", "paizuri", "ecchi", "oppai"]
    try:
        async with aiohttp.ClientSession() as session:
            if nsfw:
                tag = random.choice(nsfw_tags)
                async with session.get(f"https://api.waifu.im/search?included_tags={tag}") as response:
                    response.raise_for_status()
                    waifu_data = await response.json()
            else:
                tag = random.choice(sfw_tags)
                async with session.get(f"https://api.waifu.im/search?included_tags={tag}") as response:
                    response.raise_for_status()
                    waifu_data = await response.json()

            if waifu_data and 'images' in waifu_data and len(waifu_data['images']) > 0:
                image_url = waifu_data['images'][0]['url']
                return image_url
            else:
                return "Couldn't retrieve any waifu images right now. Please try again later!"
    except Exception as e:
        return f"Couldn't retrieve any waifu images right now. Please try again later! ({e})"