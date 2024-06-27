import asyncio
import signal
from discord import Intents, Client, Message
from models.user_profile import (get_database_connection, initialize_profile, add_xp_and_coins, display_profile, get_leaderboard, display_leaderboard_embed, place_bet, enter_lottery, draw_lottery, create_profile_table, create_bets_table, create_lottery_entries_table)
from responses import get_response
from config import TOKEN

intents: Intents = Intents.default()
intents.message_content = True
intents.messages = True
client: Client = Client(intents=intents)

async def setup_database():
    await create_profile_table()
    await create_bets_table()
    await create_lottery_entries_table()

# Initiate
@client.event
async def on_ready():
    print(f'{client.user} is now running!')
    await setup_database()

# XP & Coin Rate
XP_RATE = 5
COIN_RATE = 10
async def award_xp_and_coins(user_id, username):
    await initialize_profile(user_id, username)
    await add_xp_and_coins(user_id, XP_RATE, COIN_RATE)

# Message
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return
    
    username: str = str(message.author)
    user_message: str = message.content
    channel = message.channel

    print(f'[{channel}] {username}: "{user_message}"')

    await award_xp_and_coins(message.author.id, username)

    if user_message.startswith('!'):
        command = user_message[1:]
        response = await get_response(command, channel, str(message.author.id))
        if response:
            await message.channel.send(response)
        else:
            print("No response generated for the command.")

# Disconnect
def signal_handler(_, __):
    print("Shutting down...")
    conn = get_database_connection()
    conn.close()
    
    async def close_client():
        for vc in client.voice_clients:
            await vc.disconnect()
        await client.close()

    asyncio.run(close_client())

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def main():
    client.run(TOKEN)

if __name__ == '__main__':
    main()