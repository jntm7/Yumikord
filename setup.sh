# Python environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Node.js environment
cd emoji-translate
npm install
cd ..

echo "The setup has completed. Please proceed to add your DISCORD_TOKEN to the .env file."
