import sqlite3

conn = sqlite3.connect('user_profiles.db')
cursor = conn.cursor()

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

# XP
async def add_xp(user_id, xp_amount):
    cursor.execute('UPDATE user_profiles SET xp = xp + ? WHERE user_id = ?', (xp_amount, user_id))
    conn.commit()
    await check_level_up(user_id)

# Level Up
async def check_level_up(user_id):
    cursor.execute('SELECT xp, level FROM user_profiles WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    if result:
        xp, level = result
        level_up_xp = 100 * level
        if xp >= level_up_xp:
            new_level = level + 1
            cursor.execute('UPDATE user_profiles SET level = ? WHERE user_id = ?', (new_level, user_id))
            conn.commit()

# Level
async def get_level(user_id):
    cursor.execute('SELECT level FROM user_profiles WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    return result[0] if result else None

# Profile
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

# Coins
async def add_coins(user_id, coins_amount):
    cursor.execute('UPDATE user_profiles SET coins = coins + ? WHERE user_id = ?', (coins_amount, user_id))
    conn.commit()

# Display Profile
async def display_profile_command(user_id, channel):
    profile = await get_user_profile(user_id)
    if profile:
        await channel.send(
            f"User Profile:\n"
            f"Username: {profile['username']}\n"
            f"XP: {profile['xp']}\n"
            f"Level: {profile['level']}\n"
            f"Coins: {profile['coins']}"
        )
    else:
        await channel.send("User profile not found.")

# Add XP | Add Coins
async def add_xp_and_coins(user_id, xp_amount, coin_rate):
    await add_xp(user_id, xp_amount)
    coins_earned = xp_amount // coin_rate
    await add_coins(user_id, coins_earned)

async def add_xp_and_coins_command(user_id, xp_amount, coin_rate, channel):
    await add_xp_and_coins(user_id, xp_amount, coin_rate)
    profile = await get_user_profile(user_id)
    await channel.send(
        f"Added {xp_amount} XP and {xp_amount // coin_rate} coins to {profile['username']}.\n"
        f"New XP: {profile['xp']}\n"
        f"New Level: {profile['level']}\n"
        f"New Coins: {profile['coins']}"
    )


