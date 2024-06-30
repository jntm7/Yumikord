import discord
import yt_dlp
import asyncio
from discord import client

# YT-DLP & FFMPEG Settings
queues = {}
voice_clients = {}
yt_dlp_options = {"format": "bestaudio/best"}
ytdl = yt_dlp.YoutubeDL(yt_dlp_options)
ffmpeg_options = {'options': '-vn -filter:a "volume=0.50"'}

# Video Title
async def get_video_title(link):
    try:
        info = await asyncio.get_event_loop().run_in_executor(None, lambda: ytdl.extract_info(link, download=False))
        return info.get('title', 'Unknown Title')
    except Exception as e:
        print(f"Error getting video title: {e}")
        return 'Unknown Title'

# Audio Player
class AudioPlayer:
    def __init__(self):
        self.link_to_play = ""
        self.guild_id = None
        self.voice_clients = {}
        self.text_channels = {}

    async def enqueue(self, link, guild_id):
        if guild_id not in queues:
            queues[guild_id] = []
        title = await get_video_title(link)
        queues[guild_id].append((title, link))
        return f"Enqueued {title} to the queue."

    async def play_audio(self, link, guild_id, text_channel):
        try:
            if guild_id in self.voice_clients:
                voice_client = self.voice_clients[guild_id]
            elif client.get_guild(guild_id):
                voice_client = await client.get_guild(guild_id).voice_channels[0].connect()
                self.voice_clients[guild_id] = voice_client
            else:
                return "Guild not found."

            self.text_channels[guild_id] = text_channel
        except Exception as e:
            print(e)
            return f"Error connecting to voice channel: {e}"

        try:
            loop = asyncio.get_event_loop()
            data = await asyncio.gather(loop.run_in_executor(None, lambda: ytdl.extract_info(link, download=False)))
            song_info = data[0]
            song_url = song_info['url']
            song_title = song_info.get('title', 'Unknown Title')
            player_task = loop.create_task(self.play_audio_task(voice_client, song_url, guild_id, song_title))
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

    async def play_audio_task(self, voice_client, song, guild_id, song_title):
        try:
            player = discord.FFmpegPCMAudio(song, **ffmpeg_options)
            voice_client.play(player, after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(guild_id), client.loop))
            await self.send_now_playing_message(guild_id, song_title)
        except Exception as e:
            print(f"Error playing audio: {e}")
            raise RuntimeError(f"Error playing audio: {e}")

    async def send_now_playing_message(self, guild_id, song_title):
        if guild_id in self.text_channels:
            text_channel = self.text_channels[guild_id]
            await text_channel.send(f"Now Playing: {song_title}")

    async def play_next(self, guild_id):
        if guild_id in queues and queues[guild_id]:
            title, link = queues[guild_id].pop(0)
            await self.play_audio(link, guild_id, self.text_channels[guild_id])
        else:
            return "The queue is empty."

    async def stop_audio(self, guild_id):
        if guild_id in self.voice_clients:
            voice_client = self.voice_clients[guild_id]
            if voice_client.is_playing():
                voice_client.stop()
                return "Audio playback stopped."
            else:
                return "No audio is currently playing."
        else:
            return "Not connected to a voice channel."

audio_player = AudioPlayer()