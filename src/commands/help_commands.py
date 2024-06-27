from discord.ext import commands
from discord import Embed

class HelpCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def send_help_embed(channel, commands):
        max_fields = 25
        embeds = []
        embed = Embed(title="Help", description="Here are the commands you can use:", color=0x33B0FF)

        for i, (command, description) in enumerate(commands.items()):
            embed.add_field(name=command, value=description, inline=False)
            if (i + 1) % max_fields == 0:
                embeds.append(embed)
                embed = Embed(title="Help (continued)", color=0x00ff00)
    
        if len(embed.fields) > 0:
            embeds.append(embed)
        
        for embed in embeds:
            await channel.send(embed=embed)

    @commands.command()
    async def handle_help_command(self, ctx):
            commands = {
                "?profile": "Displays user server profile (Level, XP, Coins)",
                "?leaderboard": "Displays the top 10 highest levelled users in the server.",

                "?remind <time> <unit> <message>": "Set a reminder after a specified time with a message.",
                "calculate <expression>": "Calculates the given mathematical expression.",
                "convert <value> <from_unit> <to_unit>": "Converts a value from one unit to another.",
                "rate.<from_currency>.<to_currency>": "Fetches the exchange rate between two currencies.",
                "exchange.<amount>.<from_currency>.<to_currency>": "Converts an amount in one currency to another.",
                "crypto.<name>": "Fetches information for a specified cryptocurrency.",
                "hackernews": "Fetches the top story from Hacker News.",

                "time in <city>": "Displays the current time in the specified city.",
                "weather in <city>": "Displays the current weather in the specified city.",

                "translate <text> <source_language> <target_language>": "Translates text from one language to another.",
                "dictionary.<word>": "Defines a word.",
                "color": "Generates a random color palette.",
                "?emoji": "Translates text into emojis.",
                
                "?play <link>": "start audio playback from a specified link",
                "?pause": "pause audio playback",
                "?resume": "resume audio playback",
                "?stop": "stop audio playback",
                "?queue": "enqueue links for audio playback",
                "?viewqueue": "view queued links",

                "dice": "Rolls a 6-sided dice.",
                "coin": "Flips a 2-sided coin.",
                "number <min> <max>`": "Generates a random number between a specified range.",
                "play.rps": "Play a game of rock-paper-scissors.",
                "play.guess": "Play a game of number guessing.",
                "guess.<number>": "Input after starting the number guessing game.",
                "play.trivia": "Play a game of trivia.",
                "play.trivia <number>": "Choose numbered option as answer for trivia.",

                "joke": "Tells a random joke.",
                "dadjoke": "Tells a random dad joke.",
                "fact": "Tells a random fact.",
                "meme": "Fetches a random meme.",
                "quote": "Fetches a random quote.",
                "advice": "Fetches random advice.",
                "affirm": "Fetches a random affirmation.",
                "inspire": "Fetches a random inspirational quote.",

                "yesno": "Fetches a 'Yes' GIF or a 'No' GIF (randomized).",
                "waifu | waifu.nsfw": "Fetches a random SFW | NSFW waifu image.",
                "pokemon.<pokemon_name>": "Fetches information about the specified Pokémon.",
            }
            await self.send_help_embed(ctx.channel, commands)

    @commands.command(name='bug')
    async def handle_bug_command(self, ctx):
        response = self.bug_response()
        await ctx.send(response)

def setup(bot):
    bot.add_cog(HelpCommands(bot))