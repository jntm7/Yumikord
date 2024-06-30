import asyncio
import signal
from discord import Intents, Client, Message, commands
from responses import get_response
from config import TOKEN
from models.user_profile import (get_database_connection, initialize_profile, add_xp_and_coins, create_profile_table, create_bets_table, create_lottery_entries_table)
from commands.audio_commands import AudioCommands
from commands.profile_commands import ProfileCommands

intents: Intents = Intents.default()
intents.message_content = True
intents.messages = True

async def setup_database():
    await create_profile_table()
    await create_bets_table()
    await create_lottery_entries_table()

bot = commands.Bot(command_prefix='!', intents=intents)

# Initiate
@bot.event
async def on_ready():
    print(f'{bot.user} is now running!')
    await setup_database()
    bot.add_cog(AudioCommands(bot))
    bot.add_cog(ProfileCommands(bot))

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
    
    await bot.process_commands(message)

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