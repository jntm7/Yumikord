import sqlite3
import discord
import random
from typing import Tuple, List

# Database Connection
conn = sqlite3.connect('user_profiles.db')
cursor = conn.cursor()

def get_database_connection():
    return conn

def get_cursor():
    return cursor

# Create Profile
cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_profiles (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        xp INTEGER DEFAULT 0,
        level INTEGER DEFAULT 1,
        coins INTEGER DEFAULT 0
    )
''')
conn.commit()

# Initialize
async def initialize_profile(user_id, username):
    cursor.execute('INSERT OR IGNORE INTO user_profiles (user_id, username) VALUES (?, ?)', (user_id, username))
    conn.commit()

async def get_user_profile(user_id):
    cursor.execute('SELECT * FROM user_profiles WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    
    if result:
        return {
            'user_id': result[0],
            'username': result[1],
            'xp': result[2],
            'level': result[3],
            'coins': result[4]
        }
    return None

# Calculate XP
def calculate_xp_for_next_level(current_level: int) -> int:
    return 100 * (current_level + 1)

# Add XP & Coins
async def add_xp_and_coins(user_id, xp_amount, coin_amount):
    cursor.execute('SELECT xp, level FROM user_profiles WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()

    if result:
        current_xp, current_level = result
        new_xp = current_xp + xp_amount
        new_level = current_level + new_xp // 100
        remaining_xp = new_xp % 100

        cursor.execute('''
            UPDATE user_profiles 
            SET xp = ?, level = ?, coins = coins + ? 
            WHERE user_id = ?
        ''', (remaining_xp, new_level, coin_amount, user_id))
        conn.commit()

# Display Profile
async def display_profile(user_id, channel, client):
    profile = await get_user_profile(user_id)
    if profile:
        embed = discord.Embed(title=f"User Profile for {profile['username']}", color=0x33B0FF)

        user = await client.fetch_user(user_id)
        embed.set_thumbnail(url=user.avatar.url)

        embed.add_field(name="Level", value=str(profile['level']))
        embed.add_field(name="XP", value=f"{profile['xp']} / 100")
        embed.add_field(name="Coins", value=str(profile['coins']))
        
        if isinstance(channel, discord.TextChannel):
            await channel.send(embed=embed)
        else:
            print(f"Error: Expected discord.TextChannel, got {type(channel)}")
    else:
        if isinstance(channel, discord.TextChannel):
            await channel.send("User profile not found.")
        else:
            print(f"Error: Expected discord.TextChannel, got {type(channel)}")

# Leaderboard
async def get_leaderboard(guild: discord.Guild) -> List[Tuple[str, int, int, int]]:
    cursor = get_cursor()
    cursor.execute("""
        SELECT user_id, username, level, xp
        FROM user_profiles
        ORDER BY level DESC, xp DESC
        LIMIT 10
    """)
    leaderboard_data = cursor.fetchall()
    
    # Filter out users who are not in the guild
    guild_member_ids = [member.id for member in guild.members]
    filtered_leaderboard = [
        (username, level, xp, user_id) 
        for user_id, username, level, xp in leaderboard_data 
        if int(user_id) in guild_member_ids
    ]
    return filtered_leaderboard

# Display Leaderboard
def display_leaderboard_embed(leaderboard_data: List[Tuple[str, int, int, int]]) -> discord.Embed:
    embed = discord.Embed(title="🏆 Leaderboard", color=0xFFD700)
    
    for i, (username, level, xp, user_id) in enumerate(leaderboard_data, start=1):
        xp_to_next_level = calculate_xp_for_next_level(level)
        progress = f"{xp}/{xp_to_next_level}"
        embed.add_field(
            name=f"{i}. {username}",
            value=f"Level: {level} | XP: {progress}",
            inline=False
        )
    
    return embed

# Bets
cursor.execute('''
    CREATE TABLE IF NOT EXISTS bets (
        bet_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        bet_amount INTEGER,
        outcome INTEGER,
        is_settled BOOLEAN DEFAULT 0
    )
''')

# Lottery
cursor.execute('''
    CREATE TABLE IF NOT EXISTS lottery_entries (
        entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        entry_amount INTEGER,
        entry_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')
conn.commit()

# Bet
async def place_bet(user_id, bet_amount, bet_on):
    user_profile = await get_user_profile(user_id)
    
    if user_profile and user_profile['coins'] >= bet_amount:

        cursor.execute('UPDATE user_profiles SET coins = coins - ? WHERE user_id = ?', (bet_amount, user_id))
        conn.commit()
        
        outcome = 1 if random.random() < 0.5 else 0
        
        cursor.execute('INSERT INTO bets (user_id, bet_amount, outcome) VALUES (?, ?, ?)', (user_id, bet_amount, outcome))
        conn.commit()
        
        if outcome == 1:

            winnings = bet_amount * 2
            cursor.execute('UPDATE user_profiles SET coins = coins + ? WHERE user_id = ?', (winnings, user_id))
            conn.commit()
            return f"You won! You have gained {winnings} coins."
        else:
            return f"You lost! Better luck next time."
    else:
        return "You don't have enough coins to place this bet."

# Lottery
async def enter_lottery(user_id, entry_amount):
    user_profile = await get_user_profile(user_id)
    
    if user_profile and user_profile['coins'] >= entry_amount:

        cursor.execute('UPDATE user_profiles SET coins = coins - ? WHERE user_id = ?', (entry_amount, user_id))
        conn.commit()
        
        cursor.execute('INSERT INTO lottery_entries (user_id, entry_amount) VALUES (?, ?)', (user_id, entry_amount))
        conn.commit()
        
        return f"You have successfully entered the lottery with {entry_amount} coins."
    else:
        return "You don't have enough coins to enter the lottery."
    
# Lottery Result
async def draw_lottery():

    cursor.execute('SELECT entry_id, user_id, entry_amount FROM lottery_entries')
    entries = cursor.fetchall()
    
    if not entries:
        return "No entries in the lottery."
    
    winner_entry = random.choice(entries)
    winner_id = winner_entry[1]
    total_pot = sum(entry[2] for entry in entries)
    
    cursor.execute('UPDATE user_profiles SET coins = coins + ? WHERE user_id = ?', (total_pot, winner_id))
    conn.commit()
    
    cursor.execute('DELETE FROM lottery_entries')
    conn.commit()
    
    return f"Congratulations <@{winner_id}>! You have won the lottery with a total of {total_pot} coins!"