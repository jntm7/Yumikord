from discord.ext import commands
from src.utils.game_logic import play_rps, start_guesser, play_guesser, roll_dice, flip_coin, generate_random_number

# Game Commands
class GameCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Dice Roll Command
    @commands.command()
    async def dice(self, ctx):
        result = roll_dice()
        await ctx.send(result)

    # Coin Flip Command
    @commands.command()
    async def coin(self, ctx):
        result = flip_coin()
        await ctx.send(result)

    # Random Number Command
    @commands.command()
    async def number(self, ctx, min_val: int, max_val: int):
        result = generate_random_number(min_val, max_val)
        await ctx.send(result)

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