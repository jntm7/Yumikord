# Basic Discord Chat Bot

## Step 1: 

Create a bot on [**Discord Developer Portal**](https://discord.com/developers/applications).

If you do not already have a Discord account, sign up [here](https://discord.com/register).

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

However, you can always reset the token, just remember to replace the `DISCORD_TOKEN` value in [.env file](main/.env).

## Step 4:

Invite your bot to desired Discord server using the **OAuth2 URL Generator**:
- Navigate to `Discord Developer Portal > Settings > OAuth2`.
- Check off the "bot" scope under **OAuth2 URL Generator**

## Step 5:

Run [**main.py**](main/main.py) in IDE or code editor of your choice (such as VSCode) to launch the bot.

If there are no errors, a message such as `"YOURBOTNAME has connected successfully."` should be shown in the terminal.

## Step 6:

Send a message (in all lowercase) in any Discord channel within the Discord server you had invited the bot to.

As this is a local operation, you must keep the terminal instance running to keep the bot working. 

Terminate the instance once you want to stop, and the bot should display as offline in the Discord channel shortly after.

### Current Bot Commands:

- hello
- how are you
- roll a dice
- flip a coin
