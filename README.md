# Basic Discord Chat Bot

## Step 1: 

Create a bot on [**Discord Developer Portal**](https://discord.com/developers/applications).

If you do not already have a Discord account, sign up [here](https://discord.com/register).

## Step 2:

Find your Discord token within the Application tab of **Discord Developer Portal**.

## Step 3:

Place your Discord token into the [.env file](main/.env).

## Step 4:

Invite your bot to desired Discord server using the **OAuth2 URL Generator** on the **Discord Developer Portal**　under Settings.

## Step 5:

Run [main.py](main/main.py) in IDE or code editor of your choice (i.e. VSCode) to launch the bot.

If there are no errors, the message such as `"YOURBOTNAME has connected successfully."` should be shown in the terminal.

## Step 6:

Send a message (in all lowercase) in any Discord channel within the Discord server you had invited the bot to.

As this is a local operation, you must keep the terminal instance running to keep the bot working. 

Terminate the instance once you want to stop, and the bot should display as offline in the Discord channel shortly after.

### Current Bot Commands:

- hello
- how are you
- roll a dice
- flip a coin
