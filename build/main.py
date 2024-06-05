import os
import asyncio
import yt_dlp
import discord
from typing import Final
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response

load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
print(TOKEN)

intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)

queues = {}
voice_clients = {}
yt_dlp_options = {"format": "bestaudio/best"}
ytdl = yt_dlp.YoutubeDL(yt_dlp_options)
ffmpeg_options = {'options': '-vn -filter:a "volume=0.50"'}

# Initiate
@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running!')

# Audio Playback
class AudioPlayer:
    def __init__(self):
        self.looping = False
        self.link_to_play = ""
        self.guild_id = None
        self.voice_clients = {}

    async def start_loop(self, link_to_play, guild_id):
        self.looping = True
        self.link_to_play = link_to_play
        self.guild_id = guild_id
        await self.loop_audio()

    async def loop_audio(self):
        while self.looping:
            await self.play_audio(self.link_to_play, self.guild_id)

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
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(link, download=False))
            song = data['url']
            player = discord.FFmpegPCMAudio(song, **ffmpeg_options)
            voice_client.play(player)
        except Exception as e:
            print(e)
            return f"Error playing audio: {e}"

        return "Audio playback started."

audio_player = AudioPlayer()

## Message
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return
    
    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    print(f'[{channel}] {username}: "{user_message}"')

    # Audio Commands
    if user_message.startswith('?play'):
        if message.author.voice and message.author.voice.channel:
            link_to_play = user_message.split()[1]
            guild_id = message.guild.id
            await audio_player.play_audio(link_to_play, guild_id)
        else:
            await message.channel.send("Please join a voice channel to use this command.")

    # elif user_message.startswith('?loop'):
    #     link_to_play = user_message.split()[1]
    #     guild_id = message.guild.id
    #     await audio_player.start_loop(link_to_play, guild_id)

    # elif user_message.startswith('?endloop'):
    #     await audio_player.stop_loop()

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

def main() -> None:
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()