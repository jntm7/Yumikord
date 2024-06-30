import os
from dotenv import load_dotenv
from typing import Final

# Load Token
current_dir = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(current_dir, '..', 'build', '.env')

load_dotenv(dotenv_path)
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
print(TOKEN)