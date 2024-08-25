from discord.ext import commands
from discord import Embed
from models.user_profile import get_stats, display_stats_embed

class StatsCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def stats(self, user_id, channel):
        guild = channel.guild
        user = await self.bot.fetch_user(user_id)
        stats = await get_stats(user_id, guild.id)
        
        if stats:
            embed = display_stats_embed(user, stats)
            await channel.send(embed=embed)
        else:
            await channel.send(f"No stats available for user {user.name}")

    async def stats_other(self, user_id, channel, target_user_id):
        guild = channel.guild
        target_user = await self.bot.fetch_user(target_user_id)
        stats = await get_stats(target_user_id, guild.id)
        
        if stats:
            embed = display_stats_embed(target_user, stats)
            await channel.send(embed=embed)
        else:
            await channel.send(f"No stats available for user {target_user.name}")