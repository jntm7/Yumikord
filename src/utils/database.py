import sqlite3
import aiosqlite
from config import DATABASE_PATH

async def get_db():
    return await aiosqlite.connect(DATABASE_PATH)

async def setup_database():
    async with await get_db() as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS user_profiles (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                xp INTEGER DEFAULT 0,
                level INTEGER DEFAULT 1,
                coins INTEGER DEFAULT 0
            )
        ''')
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

    await db.commit()