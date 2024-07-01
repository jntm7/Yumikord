import sqlite3
import discord
import os
import logging
import random

# Database Connection
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "user_profiles.db")
global_conn = None

def initialize_global_connection():
    global global_conn
    try:
        global_conn = sqlite3.connect(db_path)
    except sqlite3.Error as e:
        logging.error(f"Database connection error: {e}")
        raise

def get_database_connection():
    if global_conn is None:
        initialize_global_connection()
    return global_conn

# Create Tables
async def create_profile_table():
    conn = get_database_connection()
    cursor = conn.cursor()
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

async def create_bets_table():
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bets (
            bet_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            bet_amount INTEGER,
            outcome INTEGER,
            is_settled BOOLEAN DEFAULT 0
        )
    ''')
    conn.commit()

async def create_lottery_entries_table():
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS lottery_entries (
            entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            entry_amount INTEGER,
            entry_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()

async def initialize_profile(user_id, username):
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO user_profiles (user_id, username) VALUES (?, ?)', (user_id, username))
    conn.commit()

async def get_user_profile(user_id):
    conn = get_database_connection()
    cursor = conn.cursor()
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

async def add_xp_and_coins(user_id, xp_amount, coin_amount):
    conn = get_database_connection()
    cursor = conn.cursor()
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

async def place_bet(user_id, bet_amount, bet_on):
    conn = get_database_connection()
    cursor = conn.cursor()
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
            return "You lost! Better luck next time."
    else:
        return "You don't have enough coins to place this bet."

async def enter_lottery(user_id, entry_amount):
    conn = get_database_connection()
    cursor = conn.cursor()
    user_profile = await get_user_profile(user_id)
    
    if user_profile and user_profile['coins'] >= entry_amount:
        cursor.execute('UPDATE user_profiles SET coins = coins - ? WHERE user_id = ?', (entry_amount, user_id))
        conn.commit()
        
        cursor.execute('INSERT INTO lottery_entries (user_id, entry_amount) VALUES (?, ?)', (user_id, entry_amount))
        conn.commit()
        
        return f"You have successfully entered the lottery with {entry_amount} coins."
    else:
        return "You don't have enough coins to enter the lottery."

async def draw_lottery():
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT entry_id, user_id, entry_amount FROM lottery_entries')
    entries = cursor.fetchall()
    
    if not entries:
        return "No entries in the lottery."
    
    winner_entry = random.choice(entries)
    winner_id = winner_entry[1]
    total_pot = sum(entry[2] for entry in entries)
    
    cursor.execute('UPDATE user_profiles SET coins = coins + ? WHERE user_id = ?', (total_pot, winner_id))
    conn.commit()
    
    return f"The lottery winner is user {winner_id} with a total pot of {total_pot} coins."

async def get_leaderboard():
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username, level, xp, coins FROM user_profiles ORDER BY level DESC, xp DESC LIMIT 5")
    return cursor.fetchall()

def display_leaderboard_embed(leaderboard_data):
    embed = discord.Embed(title="Leaderboard", description="Top users in the server", color=0x33B0FF)
    for rank, (username, level, xp, coins) in enumerate(leaderboard_data, start=1):
        embed.add_field(name=f"#{rank} {username}", 
                        value=f"Level: {level} | XP: {xp} | Coins: {coins}", 
                        inline=False)
    return embed