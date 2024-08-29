## 🤖 Current Bot Commands:

### 👋 Greetings

- `hello`
- `how are you`
- `bug`
- `!help` 
    - lists all available commands

### 💬 Server

- `!profile`
- `!leaderboard`
- `!user`
- `!remind <time> <unit> <message>`
    - sets a reminder after <time> <unit> where unit =
        - `seconds` (or `second`, `sec`, `s`)
        - `minutes`(or `minute`, `min`, `m`)
        - `hours` (or `hour`, `hr`, `h`)
- `bet <dice | coin> <amount>`

### 🔨 Tools

- `!calculate`: 
    - supported operations: 
        - addition (`+`)
        - subtraction (`-`)
        - multiplication (`*`)
        - division (`/`)
- `!convert`: 
    - supported unit pairs (with their associated abbreviations):
        - fahrenheit(F) + celsius (C)
        - miles (mi) + kilometres (km)
        - inches (in) + centimetres (cm)
        - feet (ft) + metres (m)
        - yards (yd) + metres (m)
        - pounds (lbs) + kilograms (kg)
        - ounces (oz) + grams (g)
        - liters (l) + gallons (gal)
- `!rate.<currency1>.<currency2>`
    - [Thanks to Frankfurter](https://www.frankfurter.app)
- `!exchange.<amount>.<currency1>.<currency2>`
    - [Thanks to Frankfurter](https://www.frankfurter.app)
- `!crypto.<name>`
    - [Thanks to CoinCap](https://docs.coincap.io)
- `!time in <city>`
    - [Thanks to WorldTimeAPI](https://worldtimeapi.org)
    - [complete list of supported timezones and cities](https://worldtimeapi.org/api/timezone/)
- `!weather in <city>`
    - [Thanks to wttr.in](https://wttr.in)
    - [complete list of supported cities](https://raw.githubusercontent.com/lutangar/cities.json/master/cities.json)
- `!hackernews`
    - [Thanks to Hacker News API (Official)](https://github.com/HackerNews/API)
- `!translate <text> <sourcelanguage> <targetlanguage>`
    - [Thanks to Google Translate API (unofficial)](https://pypi.org/project/googletrans/)   
    - [complete list of supported ISO 639 language codes](https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes) (e.g. en for English, fr for French, zh-CN for Chinese)
- `!dictionary.<word>`
    - currently only English is supported
    - [Thanks to FreeDictionaryAPI](https://dictionaryapi.dev)
- `!color`
    - [Thanks to Colormind](http://colormind.io/api/)

### 🎧 Music

Extracts and plays audio from a link in a Discord voice channel.

Thanks to [FFmpeg](https://www.ffmpeg.org) and [yt-dlp](https://github.com/yt-dlp).

- `!play <link>` - start audio playback
- `!pause` - pause audio playback
- `!resume` - resume audio playback
- `!stop` - stop audio playback
- `!queue` - enqueue links for audio playback (when already playing)
- `!endloop` - view queued links for audio playback

### 🎮 Game

- `!dice`
    - rolls a 6-sided dice
- `!coin`
    - flips a 2-sided coin
- `!number <min> <max>`
    - generates a random number within the specified range
- `!play.rps`
    - play a game of rock-paper-scissors
    - input your choice of `<rock>`, `<paper>`, or `<scissors>`
- `!play.guess`
    - play a game of number guessing
    - input your guess using `guess.<number>`
- `!play.trivia`
    - play a game of trivia
    - input your selected answer using `play.trivia <number>`
    - [Thanks to Open Trivia DB](https://opentdb.com)

### 🎉 Fun

- `!emoji`:
    - [Thanks to Emoji-Translate](http://meowni.ca/emoji-translate/)
- `!meme`:
    - [Thanks to MemeAPI](https://meme-api.com/)
- `!joke`:
    - [Thanks to JokeAPI](https://v2.jokeapi.dev/)
- `!dadjoke`:
    - [Thanks to icanhazdadjoke](https://icanhazdadjoke.com/api)
- `!quote`:
    - [Thanks to ZenQuotes](https://zenquotes.io)
- `!fact`:
    - [Thanks to UselessFacts](https://uselessfacts.jsph.pl)
- `!advice`:
    - [Thanks to Advice Slip JSON API](https://api.adviceslip.com)
- `!affirm`:
    - [Thanks to Affirmations.dev](https://affirmations.dev)
- `!inspire`:
    - [Thanks to Dictum API](https://github.com/fisenkodv/dictum)
- `!pokemon.<pokemonname>`:
    - [Thanks to PokeAPI](https://pokeapi.co/)
- `!waifu` (SFW) `waifu.nsfw` (NSFW):
    - [Thanks to Waifu.im](https://docs.waifu.im)

## ⌨️ Basic Usage Examples

### 🧮 Calculator

- ```!calcualte 9 + 10```
- ```!calculate 7 - 4```
- ```!calculate 3 x 5 ```
- ```!calculate 10 / 2```

### 🧮 Unit Converter

- ```!convert 10 mi km```         
- ```!convert 6 ft m```           
- ```!convert 12 in cm```         
- ```!convert 45 lb kg```         

### 🌡️ Temperature Converter

- ```!convert 15 c f```         
- ```!convert 85 f c```         

### 💱 Exchange Rate

- ```!rate.USD.CAD```
- ```!rate.EUR.JPY```
- ```!rate.KRW.CNY```

### 💹 Currency Converter

- ```!exchange.50.USD.CAD```
- ```!exchange.25.EUR.JPY```
- ```!exchange.10.KRW.CNY```

### 🪙 Cryptocurrency Information

- ```!crypto.bitcoin```
- ```!crypto.ethereum```
- ```!crypto.dogecoin```

### 🕒 World Clock

- ```!time in Tokyo```
- ```!time in London```
- ```!time in Shanghai```
- ```!time in New York```

### ☀️ World Weather

- ```!weather in Vancouver```
- ```!weather in Seoul```
- ```!weather in New Delhi```
- ```!weather in Madrid```

### 🗣️ Translator

- ```!translate apple en fr```             
- ```!translate ありがとう ja es```         
- ```!translate krapfen de zh-CN```        

### 🔉 Audio Playback

- ```!play https://youtu.be/dQw4w9WgXcQ```
- ```!queue https://soundcloud.com/centralcee-music/obsessed-with-you```

### 🔴 Pokémon Information

- ```!pokemon.pikachu```        
- ```!pokemon.bulbasaur```      
- ```!pokemon.charizard```     
