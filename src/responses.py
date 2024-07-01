# Import Called Functions
from utils.general import choose_random_response, no_message_response, bug_response
from utils.utility_logic import convert_units, calculator
from utils.general_api import get_time, get_weather, translate_text, get_dictionary, get_exchange_rate, convert_currency, get_crypto, get_color_palette, get_hackernews
from utils.fun_api import get_meme, get_joke, get_dadjoke, get_quote, get_fact, get_advice, get_affirmation, get_inspiration, get_yes_no_gif, get_pokemon_info, get_waifu_image
from utils.game_logic import game_states, roll_dice, flip_coin, generate_random_number, play_rps, start_guesser, play_guesser
from commands.trivia_commands import handle_trivia_command
from commands.help_commands import HelpCommands
from commands.profile_commands import ProfileCommands
from models.user_profile import handle_bet

# Global Variables
help_commands = None
profile_commands = None

# Setup Responses
def setup_responses(bot):
    global help_commands, profile_commands
    help_commands = HelpCommands(bot)
    profile_commands = ProfileCommands(bot)
 
# Get Responses
async def get_response(user_input: str, channel, user_id: str = None) -> str:
    if not user_input.startswith('!'):
        return "Commands should start with '!'"

    parts = user_input[1:].split(maxsplit=1)
    command = parts[0].lower()
    args = parts[1] if len(parts) > 1 else ""

    # No Message
    if command == '':
        return await no_message_response()

    # Profile
    elif command == 'profile':
        await profile_commands.display_profile(user_id, channel)
        return None

    # Leaderboard
    elif command == 'leaderboard':
        await profile_commands.display_leaderboard_embed(channel)
        return None
    
    # Bet
    elif command == 'bet':
        return await handle_bet(user_id, channel, args)

    # Help
    elif command == 'help':
        return await help_commands.send_help_embed(channel)

    # Bug Response
    elif command == 'bug':
        return bug_response()

    # Calculator
    elif command == 'calculate':
        return calculator(args)

    # Weather
    elif command == 'weather':
        if not args:
            return "Please provide a city name in the format: !weather <city>"
        weather_info = await get_weather(args)
        return weather_info
    
    # Time
    elif command == 'time':
        if not args:
            return "Please provide a city name in the format: !time <city>"
        timezone, time_info = await get_time(args)
        if timezone:
            return f"The current time in {timezone} is {time_info}"
        else:
            return time_info

    # Hacker News
    elif command == 'hackernews':
        return await get_hackernews()

    elif command == 'translate':
        parts = args.rsplit(maxsplit=2)
        if len(parts) < 3:
            return 'Please use the format: !translate <text> <source language> <target language>'
        text_to_translate = parts[0]
        source_language = parts[1]
        target_language = parts[2]
        translated_text, pronunciation = await translate_text(text_to_translate, source_language, target_language)
        if pronunciation:
            return f"Translated text: {translated_text}\nPronunciation: {pronunciation}"
        else:
            return f"Translated text: {translated_text}"

    # Dictionary
    elif command.startswith('dictionary.'):
        word = command.split('.', 1)[1]
        return await get_dictionary(word)

    # Unit Conversion
    elif command.startswith('convert'):
        segments = command.split(' ')
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
    elif command.startswith('rate'):
        parts = command.split('.')
        if len(parts) == 3:
            from_currency = parts[1].upper()
            to_currency = parts[2].upper()
            return await get_exchange_rate(from_currency, to_currency)
        else:
            return "Please provide the currencies in the format: rate.<currency>.<currency>."

    # Currency Conversion
    elif command.startswith('exchange'):
        parts = command.split('.')
        if len(parts) == 4:
            amount = float(parts[1])
            from_currency = parts[2].upper()
            to_currency = parts[3].upper()
            return await convert_currency(amount, from_currency, to_currency)
        else:
            return "Please provide the conversion in the format exchange.<amount>.<currency>.<currency>."

    # Cryptocurrency Price
    elif command.startswith('crypto'):
        parts = command.split('.')
        if len(parts) == 2:
            id = parts[1].lower()
            return await get_crypto(id)
        else:
            return "Please provide the cryptocurrency symbol in the format crypto.<name>."

    # Color Palette
    elif command == 'color':
        return await get_color_palette()

    # Memes
    elif command == 'meme':
        return await get_meme()
    
    # Jokes
    elif command == 'joke':
        return await get_joke()
    
    elif command == 'dadjoke':
        return await get_dadjoke()
    
    # Quotes
    elif command == 'quote':
        return await get_quote()
    
    # Facts
    elif command == 'fact':
        return await get_fact()
    
    elif command == 'advice':
        return await get_advice()
    
    # Affirmation
    elif command == 'affirm':
        return await get_affirmation()

    # Inspiration
    elif command == 'inspire':
        return await get_inspiration()
    
    # Yes / No GIF
    elif command == 'yesno':
        return await get_yes_no_gif()
    
    # Pokemon Information
    elif command.startswith('pokemon.'):
        segments = command.split('.')
        if len(segments) < 2:
            return 'Please enter a valid Pokémon.'
        pokemon_name = segments[1].strip()
        return await get_pokemon_info(pokemon_name)
    
    # Waifu Image
    elif command == 'waifu':
        return await get_waifu_image()
    elif command == 'waifu.nsfw':
        return await get_waifu_image(nsfw=True)

    # OTHER RESPONSES
    # Hello  
    elif command == 'hello':
        return "Hello! How can I help you today?"
    
    # How are you
    elif command == 'how are you':
        return "I'm doing amazing! Hope you are having a fantastic day too!"
    
    # Roll Dice
    elif command == 'dice':
        return roll_dice()
    
    # Flip Coin
    elif command == 'coin':
        return flip_coin()
    
    # Random Number
    elif 'number' in command:
        parts = command.split()
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
    elif 'rps' in command or command in ['rock', 'paper', 'scissors']:
        if user_id in game_states and game_states[user_id]['active']:
            if command in ['rock', 'paper', 'scissors']:
                return play_rps(user_id, command)
            else:
                return "Please make a move by typing '!rock', '!paper', or '!scissors'."
        elif command == 'play.rps':
            game_states[user_id] = {'active': True}
            return "Let's play Rock-Paper-Scissors! Type '!rock', '!paper', or '!scissors' to make your choice."
        else:
            return "Please start a game first by typing '!play.rps'."
    
    # Number Guesser
    elif command == 'play.guess':
        return start_guesser(user_id)

    elif command.startswith('guess.'):
        guess = command.split('guess.', 1)[1].strip()
        return play_guesser(user_id, guess)

    # Trivia
    elif command.startswith("play.trivia"):
        response = await handle_trivia_command(command)
        return response
    
    else:
        return choose_random_response(command)