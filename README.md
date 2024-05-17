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

## Step 3:

Place your Discord token into the [**.env file**](main/.env).

Keep this token secure and refrain from sharing it with anyone. 

However, you can always reset the token, just remember to replace the `DISCORD_TOKEN` value in the [.env file](main/.env).

## Step 4:

Invite your bot to desired Discord server using the **OAuth2 URL Generator**:
- Navigate to `Discord Developer Portal > Settings > OAuth2`.
- Under `OAuth2 URL Generator`, assign the `bot` scope.
- Under `Bot Permissions`, assign the bot **all the text permissions**, plus any others that you may want.

## Step 5:

Run [**main.py**](main/main.py) in IDE or code editor of your choice (such as VSCode) to launch the bot.

If there are no errors, the message `"YOURBOTNAME is now running!"` should be shown in the terminal.

## Step 6:

Send a message (in all lowercase) in any Discord channel within the Discord server you had invited the bot to. This message should be replicated in the terminal in the format `[channel] user: "message"`.

As this is a local operation, you must keep the terminal instance running to keep the bot working. 

Terminate the instance once you want to stop, and the bot should display as offline in the Discord channel shortly after.

### Current Bot Commands:

- `hello`
- `how are you`
- `roll a dice`
- `flip a coin`
- `calculate`: addition, subtraction, multiplication, division
- `time in (city)` [Thanks to WorldTimeAPI!](https://worldtimeapi.org)
    - [complete supported list of timezones and cities](https://worldtimeapi.org/api/timezone/)