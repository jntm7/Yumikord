:: Set up Python environment
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

:: Set up Node.js environment
cd emoji-translate
npm install
cd ..

echo The setup is complete. Please proceed to add your DISCORD_TOKEN to the .env file.
