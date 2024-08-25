from discord.ext import commands
from discord import Embed
from models.user_profile import get_message_count, get_stats, display_stats_embed

class StatsCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def stats(self, user_id, channel):
        user = await self.bot.fetch_user(user_id)
        guild = channel.guild
        stats = await get_stats(user_id, guild.id)
        embed = display_stats_embed(user, stats)

        await channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(StatsCommands(bot))
