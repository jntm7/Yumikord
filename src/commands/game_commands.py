from discord.ext import commands
from src.utils.game_logic import play_rps, start_guesser, play_guesser
import random

# Game Commands
class GameCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Roll Dice Command
    @commands.command()
    async def dice(self, ctx):
        result = random.randint(1, 6)
        await ctx.send(f"You rolled: {result}")

    # Flip Coin Command
    @commands.command()
    async def coin(self, ctx):
        result = random.choice(['heads', 'tails'])
        await ctx.send(f"The coin landed on: {result}")

    # Random Number Command
    @commands.command()
    async def number(self, ctx, min_val: int, max_val: int):
        result = random.randint(min_val, max_val)
        await ctx.send(f"Your random number is: {result}")

    # Rock Paper Scissors Command
    @commands.command()
    async def rps(self, ctx, user_choice):
        result = play_rps(ctx.author.id, user_choice)
        await ctx.send(result)

    # Number Guesser Command
    @commands.command()
    async def start_guesser(self, ctx):
        result = start_guesser(ctx.author.id)
        await ctx.send(result)

    @commands.command()
    async def guess(self, ctx, guess: int):
        result = play_guesser(ctx.author.id, guess)
        await ctx.send(result)

def setup(bot):
    bot.add_cog(GameCommands(bot))