from discord.ext import commands
from models.user_profile import get_leaderboard, display_leaderboard_embed, display_profile

class ProfileCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Profile Command
    async def display_profile(self, user_id, channel):
        await display_profile(user_id, channel, self.bot)

    # Leaderboard Command
    async def display_leaderboard_embed(self, channel):
        leaderboard_data = await get_leaderboard()
        if leaderboard_data:
            leaderboard_embed = display_leaderboard_embed(leaderboard_data)
            await channel.send(embed=leaderboard_embed)
        else:
            await channel.send("No leaderboard data available.")

def setup(bot):
    bot.add_cog(ProfileCommands(bot))