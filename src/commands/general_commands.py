from discord.ext import commands
from src.utils.general_api import get_weather, get_time, translate_text, get_dictionary, get_exchange_rate, convert_currency, get_crypto, get_color_palette, get_hackernews

class GeneralCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Weather Command
    @commands.command()
    async def weather(self, ctx, *, city):
        weather_info = get_weather(city)
        await ctx.send(weather_info)

    # Time Command
    @commands.command()
    async def current_time(self, ctx, *, city):
        best_match, message = await get_time(city)
        if best_match:
            await ctx.send(f'The current time in {best_match} is: {message}')
        else:
            await ctx.send(message)

    # Translate Command
    @commands.command()
    async def translate(self, ctx, source_language: str, target_language: str, *, text: str):
        translation, pronunciation = translate_text(text, source_language, target_language)
        if pronunciation:
            await ctx.send(f"Translation: {translation}\nPronunciation: {pronunciation}")
        else:
            await ctx.send(f"Translation: {translation}")
    
    # Dictionary Command
    @commands.command()
    async def dictionary(self, ctx, *, word: str):
        definition_text = get_dictionary(word)
        await ctx.send(definition_text)

    # Exchange Rate Command
    @commands.command()
    async def exchange_rate(self, ctx, from_currency: str, to_currency: str):
        rate_message = get_exchange_rate(from_currency, to_currency)
        await ctx.send(rate_message)

    # Currency Conversion Command
    @commands.command()
    async def convert(self, ctx, amount: float, from_currency: str, to_currency: str):
        conversion_message = convert_currency(amount, from_currency, to_currency)
        await ctx.send(conversion_message)

    # Crypto Command
    @commands.command()
    async def crypto(self, ctx, id: str):
        crypto_message = get_crypto(id)
        await ctx.send(crypto_message)

    # Color Palette Command
    @commands.command()
    async def color_palette(self, ctx):
        palette_message = get_color_palette()
        await ctx.send(palette_message)
    
    # HackerNews Command
    @commands.command()
    async def get_hackernews(self, ctx):
        top_story = get_hackernews()
        await ctx.send(top_story)