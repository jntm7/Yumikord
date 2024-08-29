from discord.ext import commands
from src.utils.general_api import get_meme, get_joke, get_dadjoke, get_quote, get_fact, get_advice, get_affirmation, get_inspiration, get_yes_no_gif, get_pokemon_info, get_waifu_image
from utils.emoji_translate import translate_to_emoji

class FunCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Meme Command
    @commands.command()
    async def meme(self, ctx):
        meme_url = get_meme()
        await ctx.send(meme_url)

    # Joke Command
    @commands.command()
    async def joke(self, ctx):
        joke_text = get_joke()
        await ctx.send(joke_text)

    # Dad Joke Command
    @commands.command()
    async def dadjoke(self, ctx):
        dadjoke_text = get_dadjoke()
        await ctx.send(dadjoke_text)

    # Quote Command
    @commands.command()
    async def quote(self, ctx):
        quote_text = get_quote()
        await ctx.send(quote_text)

    # Fact Command
    @commands.command()
    async def fact(self, ctx):
        fact_text = get_fact()
        await ctx.send(fact_text)

    # Advice Command
    @commands.command()
    async def advice(self, ctx):
        advice_text = get_advice()
        await ctx.send(advice_text)

    # Affirmation Command
    @commands.command()
    async def affirmation(self, ctx):
        affirmation_text = get_affirmation()
        await ctx.send(affirmation_text)

    # Inspiration Command
    @commands.command()
    async def inspiration(self, ctx):
        inspiration_text = get_inspiration()
        await ctx.send(inspiration_text)

    # Yes or No Command
    @commands.command()
    async def yesorno(self, ctx):
        yes_no_gif = get_yes_no_gif()
        await ctx.send(yes_no_gif)

    # Pokemon Command
    @commands.command()
    async def pokemon(self, ctx, pokemon_name: str):
        pokemon_info = get_pokemon_info(pokemon_name)
        await ctx.send(pokemon_info)

    # Waifu Command
    @commands.command()
    async def waifu(self, ctx, nsfw: bool = False):
        waifu_image = get_waifu_image(nsfw)
        await ctx.send(waifu_image)

    # Emoji Translate Command
    @commands.command()
    async def emoji(self, ctx, *, text: str):
        translated_text = await translate_to_emoji(text)
        await ctx.send(translated_text)

def setup(bot):
    bot.add_cog(FunCommands(bot))