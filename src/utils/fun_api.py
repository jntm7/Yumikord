import requests
import random

# Memes API
async def get_meme() -> str:
    try:
        response = requests.get("https://meme-api.com/gimme")
        response.raise_for_status()
        meme = await response.json()
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

# Dad Jokes API
def get_dadjoke() -> str:
    try:
        headers = {'Accept': 'application/json'}
        response = requests.get("https://icanhazdadjoke.com", headers = headers)
        response.raise_for_status()
        data = response.json()
        return data ['dadjoke']
    except Exception as e:
        return f"COuldn't retrieve any dad jokes right now. Please try again later! ({e})"

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
    
# Advice API
def get_advice() -> str:
    try:
        response = requests.get("https://api.adviceslip.com/advice")
        response.raise_for_status()
        data = response.json()
        advice = data['slip']['advice']
        return advice
    except Exception as e:
        return f"Couldn't retrieve any advice right now. Please try again later! ({e})"

# Affirmation API
def get_affirmation() -> str:
    try:
        response = requests.get("https://affirmations.dev")
        response.raise_for_status()
        data = response.json()
        affirmation = data['affirmation']
        return affirmation
    except Exception as e:
        return f"Couldn't retrieve any affirmations right now. Please try again later! ({e})"

# Inspiration API
def get_inspiration() -> str:
    try:
        response = requests.get("https://api.fisenko.net/v1/quotes/en/random")
        response.raise_for_status()
        data = response.json()
        inspiration = f'"{data["text"]}"\n— {data["author"]["name"]}'
        return inspiration
    except Exception as e:
        return f"Couldn't retrieve any inspiration right now. Please try again later! ({e})"

# Yes / No API
def get_yes_no_gif() -> str:
    try:
        response = requests.get("https://yesno.wtf/api")
        response.raise_for_status()
        data = response.json()
        yesno = data['image']
        return yesno
    except Exception as e:
        return f"Couldn't retrieve any yes/no GIFs right now. Please try again later! ({e})"

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