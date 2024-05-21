# Basic Discord Chat Bot

## Step 1: 

If you do not already have a Discord account, sign up [here](https://discord.com/register).

Create an application on [**Discord Developer Portal**](https://discord.com/developers/applications).

- Under `Discord Developer Portal > Applications`, click `New Application`and assign a `Name`.
- Under `Discord Developer Portal > Settings > General Information`, assign a `Description`, and `App Icon` for your application.

## Step 2:

Obtain your **Discord token** by:
- Navigate to the `Discord Developer Portal > Settings > Bot.`
- Under `Username`, there should be a `Reset Token` button.
- Before resetting, scroll down to `Privileged Gateway Intents`
- Assign the bot `MESSAGE CONTENT INTENT` (and `SERVER MEMBERS INTENT` if you choose to).
- Click `Reset Token` and complete 2FA if it is enabled on your Discord account.
- Copy your Discord token or come back to this step as we will need this in [Step 6](step-6). 

## Step 3:

Invite your bot to desired Discord server using the **OAuth2 URL Generator**:
- Navigate to `Discord Developer Portal > Settings > OAuth2`.
- Under `OAuth2 URL Generator`, assign the `bot` scope.
- Under `Bot Permissions`, assign the bot **all the text permissions**, plus any others that you may want.

## Step 4:

**Clone this repository** with your preferred version control platform (e.g. GitHub Desktop), or simply **download the code as a ZIP file** and extract it to your preferred directory.

Ensure that you have Python installed. You can download it from the [**Python official website**](https://www.python.org/downloads/). During installation, check the option to `add Python to system PATH`.

## Step 5:

Before running the program, users will need to install the required dependencies found in [** requirements.txt**](main/requirements.txt)

To do this:
- Navigate to the directory you extracted or clone the repository.
- Open a terminal or command prompt. This can be done by pressing `Win + R` then typing `cmd`.
- Assuming you have Python installed from the last step, enter ```pip install -r requirements.txt```. This will install the dependencies necessary for the features of this application.

## Step 6:

Retrieve your Discord token from the [Discord Developer Portal](https://discord.com/developers/applications) that we set up in [Step 2](#step-2).

Open [the .env file](main/.env) with a text editor (e.g. Notepad) and copy this Discord key after `DISCORD_TOKEN`.

Keep this token secure and refrain from sharing it. 

However, you can always reset the token, just remember to replace the `DISCORD_TOKEN` value in the [.env file](main/.env).

## Step 7:

Run [**main.py**](main/main.py) in IDE or code editor of your choice (e.g. VSCode) to launch the bot.

If there are no errors:
- `"YOURBOTNAME is now running!"` should be shown in the terminal.
- Your bot should appear as online in your Discord server.

## Step 8:

To interact with the bot:
- In any channel within the invited server where the bot is present, type [commands to interact with it](#current-bot-commands).
- Your typed message should be replicated in the terminal in the format `[channel] user: "message"`.

Things to note:
- As this is a local operation, you must keep the terminal instance running to keep the bot working. 
- To stop, simply terminate the command prompt or terminal. Your bot will appear as offline in Discord after a while.

## Current Bot Commands:

- `hello`
- `how are you`
- `roll a dice`
- `flip a coin`
- `calculate`: 
    - supported operations: 
        - addition
        - subtraction
        - multiplication
        - division
- `time in (city)` [Thanks to WorldTimeAPI!](https://worldtimeapi.org)
    - [complete list of supported timezones and cities](https://worldtimeapi.org/api/timezone/)
- `translate (text sourcelanguage targetlanguage)` [Thanks to Google Translate API (unofficial)](https://pypi.org/project/googletrans/)
    - [complete list of supported ISO 639 language codes](https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes) (e.g. en for English, fr for French, zh-CN for Chinese)
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

## Basic Usage Examples

### Calculator

``` calcualte 9 + 10```
``` calculate 7 - 4```
``` calculate 3 x 5 ```
``` calculate 10 / 2```

### World Clock

``` time in Tokyo```
``` time in London```
``` time in Shanghai```
``` time in New York```

### Translator

``` translate apple en fr``` translate apple in English to French
``` translate ありがとう jp es``` translate thank you in Japanese to Spanish
``` translate krapfen de zh-CN``` translate donut in German to Chinese

### Unit Converter

``` convert 10 mi km``` convert 10 miles to kilometres
``` convert 6 ft m```   convert 6 feet to metres
``` convert 12 in cm``` convert 12 inches to centimetres
``` convert 45 lb kg``` convert 45 pounds to kilograms

### Temperature Converter

``` convert 15 c f``` convert 15 Celsius to Fahrenheit
``` convert 85 f c``` convert 85 Fahrenheit to Celsius
