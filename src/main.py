import asyncio
import signal
import discord
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from discord import Intents, Message
from discord.ext.commands import Bot
from responses import get_response, setup_responses

from config import TOKEN

from models.user_profile import (get_database_connection, initialize_profile, add_xp_and_coins, create_profile_table, create_bets_table, create_stats_table, update_user_stats, update_user_roles)

intents: Intents = Intents.default()
intents.message_content = True
intents.messages = True

async def setup_database():
    await create_profile_table()
    await create_bets_table()
    await create_stats_table()

bot = Bot(command_prefix="!",intents=intents)

# XP & Coin Rate
XP_RATE = 5
COIN_RATE = 10
async def award_xp_and_coins(user_id, username):
    await initialize_profile(user_id, username)
    await add_xp_and_coins(user_id, XP_RATE, COIN_RATE)

# Load Cogs
async def setup_bot():
    bot.remove_command('help')
    cogs_dir = "src/commands"
    
    for filename in os.listdir(cogs_dir):
        if filename.endswith(".py") and filename != "__init__.py":
            cog_name = filename[:-3]
            try:
                await bot.load_extension(f"src.commands.{cog_name}")
                print(f"[cog] {cog_name} loaded successfully...")
            except Exception as e:
                print(f"Error loading cog {cog_name}: {e}")

# Initialize
@bot.event
async def on_ready():
    print(f'{bot.user} is initializing...')

    await setup_database()
    await setup_bot()

    setup_responses(bot)

    print(f'{bot.user} setup completed...')
    print(f'{bot.user} is now running!')

# Message Handling
@bot.event
async def on_message(message: Message) -> None:

    # Check if the message is from the bot
    if message.author == bot.user:
        return
    
    # Check if the message is a system message
    if message.type != discord.MessageType.default:
        return

    # Check if the message is a command
    if not message.content.startswith(bot.command_prefix):
        response = await get_response(message.content, message.channel, message.author.id)
        if response:
            await message.channel.send(response)

    await award_xp_and_coins(message.author.id, str(message.author))
    await bot.process_commands(message)

    username: str = str(message.author)
    user_message: str = message.content
    channel = message.channel

    print(f'[{channel}] {username}: "{user_message}"')

# Member Join
@bot.event
async def on_member_join(member):
    await update_user_stats(member)

# Role Update
@bot.event
async def on_member_update(before, after):
    if before.roles != after.roles:
        await update_user_roles(after.id, after.guild.id, after.roles)

# Disconnect
def signal_handler(_, __):
    print(f'{bot.user} and connections are shutting down...')
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
    bot.loop.run_until_complete(setup_bot())
    bot.run(TOKEN)

if __name__ == '__main__':
    main()
