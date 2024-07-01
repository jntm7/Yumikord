from discord.ext import commands
from models.user_profile import place_bet, enter_lottery, draw_lottery, get_leaderboard, display_leaderboard_embed, display_profile

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

    # Bet Command
    @commands.command()
    async def bet(self, ctx, amount: int):
        response = await place_bet(ctx.author.id, amount)
        await ctx.send(response)

    # Lottery Command
    @commands.command()
    async def lottery(self, ctx, amount: int):
        response = await enter_lottery(ctx.author.id, amount)
        await ctx.send(response)

    # Draw Lottery Command
    @commands.command()
    async def drawlottery(self, ctx):
        if any(role.permissions.administrator for role in ctx.author.roles):
            response = await draw_lottery()
            await ctx.send(response)
        else:
            await ctx.send("You do not have permission to draw the lottery.")