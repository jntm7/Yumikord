import asyncio
import signal
from discord import Intents, Message
from discord.ext.commands import Bot
from responses import get_response, setup_responses
from config import TOKEN
from models.user_profile import (get_database_connection, initialize_profile, add_xp_and_coins, create_profile_table, create_bets_table)
from commands.audio_commands import AudioCommands
from commands.profile_commands import ProfileCommands
from commands.help_commands import HelpCommands

intents: Intents = Intents.default()
intents.message_content = True
intents.messages = True

async def setup_database():
    await create_profile_table()
    await create_bets_table()

bot = Bot(command_prefix="!",intents=intents)

# Initiate
@bot.event
async def on_ready():
    print(f'{bot.user} is now running!')

    await setup_database()

    setup_responses(bot)

    bot.remove_command('help')

    await bot.add_cog(AudioCommands(bot))
    await bot.add_cog(ProfileCommands(bot))
    await bot.add_cog(HelpCommands(bot))

# XP & Coin Rate
XP_RATE = 5
COIN_RATE = 10
async def award_xp_and_coins(user_id, username):
    await initialize_profile(user_id, username)
    await add_xp_and_coins(user_id, XP_RATE, COIN_RATE)

# Message
@bot.event
async def on_message(message: Message) -> None:
    if message.author == bot.user:
        return
    
    response = await get_response(message.content, message.channel, message.author.id)
    if response:
        await message.channel.send(response)

    username: str = str(message.author)
    user_message: str = message.content
    channel = message.channel

    print(f'[{channel}] {username}: "{user_message}"')

    await award_xp_and_coins(message.author.id, username)

# Disconnect
def signal_handler(_, __):
    print("Shutting down...")
    conn = get_database_connection()
    conn.close()
    
    loop = asyncio.get_event_loop()
    tasks = [vc.disconnect() for vc in bot.voice_clients]
    tasks.append(bot.close())

    if loop.is_running():
        loop.create_task(asyncio.wait(tasks))
    else:
        loop.run_until_complete(asyncio.wait(tasks))

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def main():
    bot.run(TOKEN)

if __name__ == '__main__':
    main()