from discord.ext import commands
from models.user_profile import place_bet, enter_lottery, draw_lottery, get_leaderboard, display_leaderboard_embed, display_profile

class ProfileCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Profile Command
    @commands.command()
    async def profile(self, ctx):
        await display_profile(ctx.author.id, ctx.channel, self.bot)

    # Leaderboard Command
    @commands.command()
    async def leaderboard(self, ctx):
        guild = ctx.guild
        leaderboard_data = await get_leaderboard(guild)
        if leaderboard_data:
            leaderboard_embed = display_leaderboard_embed(leaderboard_data)
            await ctx.send(embed=leaderboard_embed)
        else:
            await ctx.send("No leaderboard data available.")

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