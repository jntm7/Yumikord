# Yumikord

![image](https://github.com/jntm7/Yumikord/assets/108718802/349a4bbf-e7fd-443b-9c65-b07761743934)

*Elevate your Discord community with **Yumiko** - a versatile and multifunctional bot!*

## 🛠️ Installation & Setup

### 🔨 Step 1: 

If you do not already have a Discord account, sign up [here](https://discord.com/register).

Create an application on [**Discord Developer Portal**](https://discord.com/developers/applications).

- Under `Discord Developer Portal > Applications`, click `New Application`and assign a `Name`.
- Under `Discord Developer Portal > Settings > General Information`, assign a `Description`, and `App Icon` for your application.

### 🔨 Step 2:

Obtain your **Discord token** by:
- Navigate to the `Discord Developer Portal > Settings > Bot.`
- Under `Username`, there should be a `Reset Token` button.
- Before resetting, scroll down to `Privileged Gateway Intents`
- Assign the bot `MESSAGE CONTENT INTENT` (and `SERVER MEMBERS INTENT` if you choose to).
- Click `Reset Token` and complete 2FA if it is enabled on your Discord account.
- Copy your Discord token or come back to this step as we will need this in [Step 6](https://github.com/jntm7/discord-chatbot-catto?tab=readme-ov-file#step-6). 

### 🔨 Step 3:

Invite your bot to desired Discord server using the **OAuth2 URL Generator**:
- Navigate to `Discord Developer Portal > Settings > OAuth2`.
- Under `OAuth2 URL Generator`, assign the `bot` scope.
- Under `Bot Permissions`, assign the bot **all the text permissions**, as well as **connect, speak under voice permissions**.

### 🔨 Step 4:

**Clone this repository** with your preferred version control platform (e.g. GitHub Desktop), or simply **download [build](build)** and place it to your preferred directory.

Ensure that you have Python installed. You can download it from the [**Python official website**](https://www.python.org/downloads/). During installation, check the option to `add Python to system PATH`.

### 🔨 Step 5:

Before running the program, users will need to install the required dependencies found in [**requirements.txt**](build/requirements.txt)

To do this:
- Navigate to the directory you extracted or clone the repository.
- Open a terminal or command prompt. This can be done by pressing `Win + R` then typing `cmd`.
- Assuming you have Python installed from the last step, enter ```pip install -r requirements.txt```. This will install the dependencies necessary for the features of this application.

### 🔨 Step 6:

Retrieve your Discord token from the [Discord Developer Portal](https://discord.com/developers/applications) that we set up in [Step 2](#step-2).

Open the [.env file](build/.env) with a text editor (e.g. Notepad) and copy this Discord key after `DISCORD_TOKEN`.

Keep this token secure and refrain from sharing it. 

However, you can always reset the token, just remember to replace the `DISCORD_TOKEN` value in the [.env file](build/.env).

### 🔨 Step 7:

Run [**main.py**](build/main.py) in IDE or code editor of your choice (e.g. VSCode) to launch the bot.

If there are no errors:
- `"YOURBOTNAME is now running!"` should be shown in the terminal.
- Your bot should appear as online in your Discord server.

### 🔨 Step 8:

To interact with the bot:
- In any channel within the invited server where the bot is present, type [commands to interact with it](#current-bot-commands).
- Your typed message should be replicated in the terminal in the format `[channel] user: "message"`.

Things to note:
- As this is a local operation, you must keep the terminal instance running to keep the bot working. 
- To stop, simply terminate the command prompt or terminal. Your bot will appear as offline in Discord after a while.

## 🤖 Current Bot Commands:

### 👋 Greetings

- `hello`
- `how are you`
- `help` - to prompt the bot to list all its available commands

### 🔨 Tools

- `calculate`: 
    - supported operations: 
        - addition (`+`)
        - subtraction (`-`)
        - multiplication (`*`)
        - division (`/`)
- `convert`: 
    - supported unit pairs (with their associated abbreviations):
        - fahrenheit(F) + celsius (C)
        - miles (mi) + kilometres (km)
        - inches (in) + centimetres (cm)
        - feet (ft) + metres (m)
        - yards (yd) + metres (m)
        - pounds (lbs) + kilograms (kg)
        - ounces (oz) + grams (g)
        - liters (l) + gallons (gal)
- `rate.<currency1>.<currency2>`
    - [Thanks to Frankfurter](https://www.frankfurter.app)
- `exchange.<amount>.<currency1>.<currency2>`
    - [Thanks to Frankfurter](https://www.frankfurter.app)
- `crypto.<name>`
    - [Thanks to CoinCap](https://docs.coincap.io)
- `time in <city>`
    - [Thanks to WorldTimeAPI](https://worldtimeapi.org)
    - [complete list of supported timezones and cities](https://worldtimeapi.org/api/timezone/)
- `weather in <city>`
    - [Thanks to wttr.in](https://wttr.in)
    - [complete list of supported cities](https://raw.githubusercontent.com/lutangar/cities.json/master/cities.json)
- `hackernews`
    - [Thanks to Hacker News API (Official)](https://github.com/HackerNews/API)
- `translate <text> <sourcelanguage> <targetlanguage>`
    - [Thanks to Google Translate API (unofficial)](https://pypi.org/project/googletrans/)   
    - [complete list of supported ISO 639 language codes](https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes) (e.g. en for English, fr for French, zh-CN for Chinese)
- `dictionary.<word>`
    - currently only English is supported
    - [Thanks to FreeDictionaryAPI](https://dictionaryapi.dev)
- `color`
    - [Thanks to Colormind](http://colormind.io/api/)

### 🎧 Music

Extracts and plays audio from a link in a Discord voice channel.

Thanks to [FFmpeg](https://www.ffmpeg.org) and [yt-dlp](https://github.com/yt-dlp).

- `?play <link>` - start audio playback
- `?pause` - pause audio playback
- `?resume` - resume audio playback
- `?stop` - stop audio playback
- `?loop` - loop audio playback
- `?endloop` - stop looping audio playback

### 🎮 Game

- `dice`
    - rolls a 6-sided dice
- `coin`
    - flips a 2-sided coin
- `number <min> <max>`
    - generates a random number within the specified range
- `play.rps`
    - play a game of rock-paper-scissors
    - input your choice of `<rock>` , `<paper>`, or `<scissors>`
- `play.guess`
    - play a game of number guessing
    - input your guess using `guess.<number>`

### 🎉 Fun

- `meme`:
    - [Thanks to MemeAPI](https://meme-api.com/)
- `joke`:
    - [Thanks to JokeAPI](https://v2.jokeapi.dev/)
- `dadjoke`:
    - [Thanks to icanhazdadjoke](https://icanhazdadjoke.com/api)
- `quote`:
    - [Thanks to ZenQuotes](https://zenquotes.io)
- `fact`:
    - [Thanks to UselessFacts](https://uselessfacts.jsph.pl)
- `advice`:
    - [Thanks to Advice Slip JSON API](https://api.adviceslip.com)
- `affirm`:
    - [Thanks to Affirmations.dev](https://affirmations.dev)
- `inspire`:
    - [Thanks to Dictum API](https://github.com/fisenkodv/dictum)
- `pokemon.<pokemonname>`:
    - [Thanks to PokeAPI](https://pokeapi.co/)
- `waifu` (SFW) `waifu.nsfw` (NSFW):
    - [Thanks to Waifu.im](https://docs.waifu.im)

## ⌨️ Basic Usage Examples

### 🧮 Calculator

- ```calcualte 9 + 10```
- ```calculate 7 - 4```
- ```calculate 3 x 5 ```
- ```calculate 10 / 2```

### 🧮 Unit Converter

- ```convert 10 mi km```         
- ```convert 6 ft m```           
- ```convert 12 in cm```         
- ```convert 45 lb kg```         

### 🌡️ Temperature Converter

- ```convert 15 c f```         
- ```convert 85 f c```         

### 💱 Exchange Rate

- ```rate.USD.CAD```
- ```rate.EUR.JPY```
- ```rate.KRW.CNY```

### 💹 Currency Converter

- ```exchange.50.USD.CAD```
- ```exchange.25.EUR.JPY```
- ```exchange.10.KRW.CNY```

### 🪙 Cryptocurrency Information

- ```crypto.bitcoin```
- ```crypto.ethereum```
- ```crypto.dogecoin```

### 🕒 World Clock

- ```time in Tokyo```
- ```time in London```
- ```time in Shanghai```
- ```time in New York```

### ☀️ World Weather

- ```weather in Vancouver```
- ```weather in Seoul```
- ```weather in New Delhi```
- ```weather in Madrid```

### 🗣️ Translator

- ```translate apple en fr```             
- ```translate ありがとう jp es```         
- ```translate krapfen de zh-CN```        

### 🔉 Audio Playback

- ```?play https://youtu.be/dQw4w9WgXcQ```
- ```?play https://soundcloud.com/centralcee-music/obsessed-with-you```

### 🔴 Pokémon Information

- ```pokemon.pikachu```        
- ```pokemon.bulbasaur```      
- ```pokemon.charizard```      
