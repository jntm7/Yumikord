from discord.ext import commands
from utils.audio_player import AudioPlayer

# Audio Commands
class AudioCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.audio_player = AudioPlayer(bot)

    @commands.command(name='play')
    async def play(self, ctx, *, link_to_play: str = None):
        if ctx.author.voice and ctx.author.voice.channel:
            if link_to_play:
                guild_id = ctx.guild.id
                response = await self.audio_player.play_audio(link_to_play, guild_id, ctx.channel)
                await ctx.send(response)
            else:
                await ctx.send("Please provide a valid URL to play.")
        else:
            await ctx.send("Please join a voice channel to use this command.")

    @commands.command(name='pause')
    async def pause(self, ctx):
        if ctx.author.voice and ctx.author.voice.channel:
            await self.audio_player.pause_audio(ctx.guild.id)
        else:
            await ctx.send("Please join a voice channel to use this command.")

    @commands.command(name='resume')
    async def resume(self, ctx):
        if ctx.author.voice and ctx.author.voice.channel:
            await self.audio_player.resume_audio(ctx.guild.id)
        else:
            await ctx.send("Please join a voice channel to use this command.")

    @commands.command(name='stop')
    async def stop(self, ctx):
        if ctx.author.voice and ctx.author.voice.channel:
            response = await self.audio_player.stop_audio(ctx.guild.id)
            await ctx.send(response)
        else:
            await ctx.send("Please join a voice channel to use this command.")

    @commands.command(name='queue')
    async def queue(self, ctx, *, link_to_queue: str = None):
        if ctx.author.voice and ctx.author.voice.channel:
            if link_to_queue:
                guild_id = ctx.guild.id
                enqueue_message = await self.audio_player.enqueue(link_to_queue, guild_id)
                await ctx.send(enqueue_message)
            else:
                await ctx.send("Please provide a valid URL to enqueue.")
        else:
            await ctx.send("Please join a voice channel to use this command.")

    @commands.command(name='viewqueue')
    async def viewqueue(self, ctx):
        guild_id = ctx.guild.id
        queue = self.audio_player.get_queue(guild_id)
        if queue:
            queue_message = "Current queue:\n"
            for i, (title, link) in enumerate(queue, start=1):
                queue_message += f"{i}. **{title.ljust(15)}** [<{link}>]\n"
        else:
            queue_message = "The queue is currently empty."
        await ctx.send(queue_message)

def setup(bot):
    bot.add_cog(AudioCommands(bot))