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

# Create Profile
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

# Create Bets
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

# Initialize Profile
async def initialize_profile(user_id, username):
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO user_profiles (user_id, username) VALUES (?, ?)', (user_id, username))
    conn.commit()

# Get Profile
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

# Add XP & Coins
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
async def get_leaderboard():
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username, level, xp, coins FROM user_profiles ORDER BY level DESC, xp DESC LIMIT 5")
    return cursor.fetchall()

# Display Leaderboard
def display_leaderboard_embed(leaderboard_data):
    embed = discord.Embed(title="Leaderboard", description="Top users in the server", color=0x33B0FF)
    for rank, (username, level, xp, coins) in enumerate(leaderboard_data, start=1):
        embed.add_field(name=f"#{rank} {username}", 
                        value=f"Level: {level} | XP: {xp} | Coins: {coins}", 
                        inline=False)
    return embed

# Stats
async def get_stats(user_id, guild_id):
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT joined_at, roles, message_count FROM user_stats WHERE user_id = ? AND guild_id = ?", (user_id, guild_id))
    result = cursor.fetchone()
    if result:
        joined_at, roles, message_count = result
        return {
            "joined_at": joined_at,
            "roles": roles.split(",") if roles else [],
            "message_count": message_count
        }
    return None

# Display Stats
def display_stats_embed(user, stats):
    if not stats:
        return discord.Embed(title="Stats", description="No stats available for this user.", color=0xFF0000)

    embed = discord.Embed(title=f"Stats for {user.display_name}", color=0x33B0FF)
    embed.set_thumbnail(url=user.avatar.url)
    embed.add_field(name="Joined At", value=stats["joined_at"], inline=False)
    embed.add_field(name="Roles", value=", ".join(stats["roles"]) if stats["roles"] else "No roles", inline=False)
    embed.add_field(name="Message Count", value=str(stats["message_count"]), inline=False)

    return embed

# Create Stats Table
async def create_stats_table():
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_stats (
            user_id INTEGER,
            guild_id INTEGER,
            joined_at TEXT,
            roles TEXT,
            message_count INTEGER DEFAULT 0,
            PRIMARY KEY (user_id, guild_id)
        )
    ''')
    conn.commit()

# Add Message Count
async def increment_message_count(user_id, guild_id):
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO user_stats (user_id, guild_id, message_count) VALUES (?, ?, 1) ON CONFLICT(user_id, guild_id) DO UPDATE SET message_count = message_count + 1', (user_id, guild_id))
    conn.commit()

######################################################

# Bet Logic
async def update_user_coins(user_id, amount):
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE user_profiles SET coins = coins + ? WHERE user_id = ?', (amount, user_id))
    conn.commit()

async def insert_bet_record(user_id, bet_amount, user_won, bet_on):
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO bets (user_id, bet_amount, outcome, bet_on) VALUES (?, ?, ?, ?)', (user_id, bet_amount, int(user_won), int(bet_on)))
    conn.commit()

async def place_bet(user_id, bet_amount, bet_on, bet_type):
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT coins FROM user_profiles WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()

    if result:
        current_coins = result[0]
        if current_coins >= bet_amount:
            await update_user_coins(user_id, -bet_amount)
            
            actual_outcome = random.choice([True, False]) if bet_type == 'coin' else random.randint(1, 6)
            user_won = (bet_on == actual_outcome) if bet_type == 'coin' else (int(bet_on) == actual_outcome)

            await insert_bet_record(user_id, bet_amount, user_won, bet_on)
            if user_won:
                winnings_multiplier = 6 if bet_type == 'dice' else 2
                winnings = bet_amount * winnings_multiplier
                await update_user_coins(user_id, winnings)
                return f"You won! You have gained {winnings} coins."
            else:
                return "You lost! Better luck next time."
        else:
            return "You don't have enough coins to place this bet."
    else:
        return "User profile not found."

async def handle_bet(user_id: str, channel, args: str):
    args_parts = args.split()
    
    if len(args_parts) >= 3 and args_parts[0].isdigit():
        amount = int(args_parts[0])
        bet_type = args_parts[1].lower()
        bet_on = args_parts[2].lower()

        valid_bet_types = {'dice': range(1, 7), 'coin': ['heads', 'tails']}
        if bet_type not in valid_bet_types:
            await channel.send("Invalid bet type. Please choose 'dice' or 'coin'.")
            return

        if bet_type == 'dice' and (not bet_on.isdigit() or int(bet_on) not in valid_bet_types[bet_type]):
            await channel.send("For dice bets, please bet on a number between 1 and 6.")
            return
        elif bet_type == 'coin' and bet_on not in valid_bet_types[bet_type]:
            await channel.send("For coin bets, please bet on 'heads' or 'tails'.")
            return

        bet_result_message = await place_bet(user_id, amount, bet_on, bet_type)
        await channel.send(bet_result_message)
    else:
        await channel.send("Please place a bet in the format: !bet <amount> <dice|coin> <target>")