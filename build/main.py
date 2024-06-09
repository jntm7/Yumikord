import os
import asyncio
import yt_dlp
import discord
import signal
import sys
from typing import Final
from dotenv import load_dotenv
from discord import Intents, Client, Message, Embed
from responses import get_response, choose_random_response

load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
print(TOKEN)

intents: Intents = Intents.default()
intents.message_content = True
intents.messages = True
client: Client = Client(intents=intents)

queues = {}
voice_clients = {}
yt_dlp_options = {"format": "bestaudio/best"}
ytdl = yt_dlp.YoutubeDL(yt_dlp_options)
ffmpeg_options = {'options': '-vn -filter:a "volume=0.50"'}

async def get_video_title(link):
    try:
        info = await asyncio.get_event_loop().run_in_executor(None, lambda: ytdl.extract_info(link, download=False))
        return info.get('title', 'Unknown Title')
    except Exception as e:
        print(f"Error getting video title: {e}")
        return 'Unknown Title'

# Initiate
@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running!')

# Help
async def send_help_embed(channel, commands):
    max_fields = 25
    embeds = []
    embed = Embed(title="Help", description="Here are the commands you can use:", color=0x00ff00)

    for i, (command, description) in enumerate(commands.items()):
        embed.add_field(name=command, value=description, inline=False)
        if (i + 1) % max_fields == 0:
            embeds.append(embed)
            embed = Embed(title="Help (continued)", color=0x00ff00)
  
    if len(embed.fields) > 0:
        embeds.append(embed)
    
    for embed in embeds:
        await channel.send(embed=embed)

# Audio Player
class AudioPlayer:
    def __init__(self):
        self.link_to_play = ""
        self.guild_id = None
        self.voice_clients = {}

    async def enqueue(self, link, guild_id):
        if guild_id not in queues:
            queues[guild_id] = []
        title = await get_video_title(link)
        queues[guild_id].append((title, link))
        return f"Enqueued {title} to the queue."

    async def play_audio(self, link, guild_id):
        try:
            if guild_id in self.voice_clients:
                voice_client = self.voice_clients[guild_id]
            elif client.get_guild(guild_id):
                voice_client = await client.get_guild(guild_id).voice_channels[0].connect()
                self.voice_clients[guild_id] = voice_client
            else:
                return "Guild not found."
        except Exception as e:
            print(e)
            return f"Error connecting to voice channel: {e}"

        try:
            loop = asyncio.get_event_loop()
            data = await asyncio.gather(loop.run_in_executor(None, lambda: ytdl.extract_info(link, download=False)))
            song = data[0]['url']
            player_task = loop.create_task(self.play_audio_task(voice_client, song, guild_id))
            await player_task
        except KeyError:
            return "Unable to find audio URL."
        except discord.ClientException as e:
            return f"Discord client exception: {e}"
        except discord.DiscordException as e:
            return f"Discord exception: {e}"
        except Exception as e:
            print(e)
            return f"Error playing audio: {e}"

        return "Audio playback started."
    
    async def play_audio_task(self, voice_client, song, guild_id):
        try:
            player = discord.FFmpegPCMAudio(song, **ffmpeg_options)
            voice_client.play(player, after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(guild_id), client.loop))
        except Exception as e:
            print(f"Error playing audio: {e}")
            raise RuntimeError(f"Error playing audio: {e}")

    async def play_next(self, guild_id):
        if guild_id in queues and queues[guild_id]:
            link = queues[guild_id].pop(0)
            await self.play_audio(link, guild_id)
        else:
            return "The queue is empty."

audio_player = AudioPlayer()

# Reminder
reminders = {}

def parse_reminder(reminder_text):
    try:
        parts = reminder_text.split()
        time_str = parts[0]
        unit = parts[1].lower()
        message = ' '.join(parts[2:])

        if unit == 'seconds' or unit == 'second' or unit == 'sec' or unit == 's':
            delay = int(time_str)
        elif unit == 'minutes' or unit == 'minute' or unit == 'min' or unit == 'm':
            delay = int(time_str) * 60
        elif unit == 'hours' or unit == 'hour' or unit == 'hr' or unit == 'h':
            delay = int(time_str) * 3600
        else:
            return None, None
        return delay, message
    except (ValueError, IndexError):
        return None, None

async def send_reminder(user_id, channel_id, message):
    channel = client.get_channel(int(channel_id))
    mention = f"<@{user_id}>"
    await channel.send(f"{mention} Reminder: {message}")

async def send_reminder_delayed(delay, user_id, channel_id, message):
    await asyncio.sleep(delay)
    await send_reminder(user_id, channel_id, message)

async def schedule_reminder(delay, user_id, channel_id, message):
    reminder_task = asyncio.create_task(send_reminder_delayed(delay, user_id, channel_id, message))
    reminders[reminder_task] = (user_id, channel_id, message)

## Message
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return
    
    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)
    guild_id = message.guild.id

    print(f'[{channel}] {username}: "{user_message}"')

    # Help
    if user_message.startswith('?help'):
        commands = {
            "?remind <time> <unit> <message>": "Set a reminder after a specified time with a message.",
            "calculate <expression>": "Calculates the given mathematical expression.",
            "convert <value> <from_unit> <to_unit>": "Converts a value from one unit to another.",
            "rate.<from_currency>.<to_currency>": "Fetches the exchange rate between two currencies.",
            "exchange.<amount>.<from_currency>.<to_currency>": "Converts an amount in one currency to another.",
            "crypto.<name>": "Fetches information for a specified cryptocurrency.",
            "hackernews": "Fetches the top story from Hacker News.",

            "time in <city>": "Displays the current time in the specified city.",
            "weather in <city>": "Displays the current weather in the specified city.",

            "translate <text> <source_language> <target_language>": "Translates text from one language to another.",
            "dictionary.<word>": "Defines a word.",
            "color": "Generates a random color palette.",
            
            "?play <link>": "start audio playback from a specified link",
            "?pause": "pause audio playback",
            "?resume": "resume audio playback",
            "?stop": "stop audio playback",
            "?queue": "enqueue links for audio playback",
            "?viewqueue": "view queued links",

            "dice": "Rolls a 6-sided dice.",
            "coin": "Flips a 2-sided coin.",
            "number <min> <max>`": "Generates a random number between a specified range.",
            "play.rps": "Play a game of rock-paper-scissors.",
            "play.guess": "Play a game of number guessing.",
            "guess.<number>": "Input after starting the number guessing game.",

            "joke": "Tells a random joke.",
            "dadjoke": "Tells a random dad joke.",
            "fact": "Tells a random fact.",
            "meme": "Fetches a random meme.",
            "quote": "Fetches a random quote.",
            "advice": "Fetches random advice.",
            "affirm": "Fetches a random affirmation.",
            "inspire": "Fetches a random inspirational quote.",

            "yesno": "Fetches a 'Yes' GIF or a 'No' GIF (randomized).",
            "waifu | waifu.nsfw": "Fetches a random SFW | NSFW waifu image.",
            "pokemon.<pokemon_name>": "Fetches information about the specified Pokémon.",
        }
        await send_help_embed(message.channel, commands)

    # Audio Commands
    if user_message.startswith('?play'):
        if message.author.voice and message.author.voice.channel:
            split_message = user_message.split()
            if len(split_message) > 1:
                link_to_play = split_message[1]
                guild_id = message.guild.id
                await audio_player.play_audio(link_to_play, guild_id)
            else:
                await message.channel.send("Please provide a valid URL to play.")
        else:
            await message.channel.send("Please join a voice channel to use this command.")

    elif user_message.startswith('?loop'):
        link_to_play = user_message.split()[1]
        guild_id = message.guild.id
        await audio_player.start_loop(link_to_play, guild_id)

    elif user_message.startswith('?endloop'):
        await audio_player.stop_loop()

    elif user_message.startswith('?pause'):
        if message.author.voice and message.author.voice.channel:
            await audio_player.pause_audio(message.guild.id)
        else:
            await message.channel.send("Please join a voice channel to use this command.")

    elif user_message.startswith('?resume'):
        if message.author.voice and message.author.voice.channel:
            await audio_player.resume_audio(message.guild.id)
        else:
            await message.channel.send("Please join a voice channel to use this command.")

    elif user_message.startswith('?stop'):
        if message.author.voice and message.author.voice.channel:
            await audio_player.stop_audio(message.guild.id)
        else:
            await message.channel.send("Please join a voice channel to use this command.")

    elif user_message.startswith('?queue'):
        if message.author.voice and message.author.voice.channel:
            split_message = user_message.split()
            if len(split_message) > 1:
                link_to_queue = split_message[1]
                enqueue_message = await audio_player.enqueue(link_to_queue, guild_id)
                await message.channel.send(enqueue_message)
            else:
                await message.channel.send("Please provide a valid URL to enqueue.")
        else:
            await message.channel.send("Please join a voice channel to use this command.")

    elif user_message.startswith('?viewqueue'):
        guild_id = message.guild.id
        queue = queues.get(guild_id, [])
        if queue:
            queue_message = "Current queue:\n" + "\n".join([f"**{title}**\n<{link}>" for title, link in queue])
        else:
            queue_message = "The queue is currently empty."
        await message.channel.send(queue_message)

    # Reminder
    elif user_message.startswith('?remind'):
        reminder_text = ' '.join(user_message.split()[1:])
        delay, reminder_message = parse_reminder(reminder_text)
        if delay is None or reminder_message is None:
            await message.channel.send("Invalid reminder format. Please use: ?remind <time> <unit> <message>")
        else:
            await schedule_reminder(delay, str(message.author.id), str(message.channel.id), reminder_message)
            await message.channel.send(f"Reminder set for {delay} seconds: {reminder_message}. I'll notify you when the time is up.")

    else:
        response = get_response(user_message, str(message.author.id))
        await message.channel.send(response)

## No Message
async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print('(Message was empty because intents were not enabled properly.)')
        return
    if is_private := user_message[0] == '?':
        user_message = user_message[1:]
    try:
        response: str = get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

# Disconnect
def signal_handler(sig, frame):
    print("Shutting down...")
    async def close_client():
        for vc in client.voice_clients:
            await vc.disconnect()
        await client.close()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(close_client())
    sys.exit(0)

def main() -> None:
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()