from discord.ext import commands
from utils.utility_logic import convert_units_logic, calculator

class UtilityCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Unit Converter Command
    @commands.command()
    async def convert_units(self, ctx, value: float, from_unit: str, to_unit: str):
        result_message = await convert_units_logic(value, from_unit, to_unit)
        await ctx.send(result_message)

    # Calculator Command
    @commands.command()
    async def calculate_command(self, ctx, *, user_input: str):
        result = calculator(user_input)
        await ctx.send(result)

def setup(bot):
    bot.add_cog(UtilityCommands(bot))