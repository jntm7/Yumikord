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
- Copy your Discord token that will be needed in Step 6. 

### 🔨 Step 3:

Invite your bot to desired Discord server using the **OAuth2 URL Generator**:
- Navigate to `Discord Developer Portal > Settings > OAuth2`.
- Under `OAuth2 URL Generator`, assign the `bot` scope.
- Under `Bot Permissions`, assign the bot **all the text permissions**, as well as **connect, speak under voice permissions**.

### 🔨 Step 4:

Please ensure that you have the necessary prerequisites; Python and Node.js installed.

**Prerequisites:**
   - [Python](https://python.org/downloads/) (3.7 or higher)
   - [Node.js](https://nodejs.org/en) (includes npm)

### 🔨 Step 5:

**Installation:**

- Clone this repository or download the source code.

- Navigate to the project directory in your terminal.

- Install Python dependencies:
    ```
    pip install -r requirements.txt
    ```

- Install Node.js dependencies:
    ```
    cd emoji-translate
    npm install
    cd ..
    ```

### 🔨 Step 6:

- Retrieve your Discord token from the [Discord Developer Portal](https://discord.com/developers/applications) that we set up in Step 2.

- Open the [.env file](build\.env) with a text editor (e.g. Notepad) and add your Discord token: ```DISCORD_TOKEN=your_token_here```.

**Keep this token secure** and refrain from sharing it, as it will grant anyone with it unrestricted access to your bot and server.

### 🔨 Step 7:

- Run the bot:
      ```
      python src/main.py
      ```
- If successful, you'll see "YOURBOTNAME is now running!" in the terminal.
- Your bot should appear online in your Discord server.

### 🔨 Step 8:

To interact with the bot:
- Use [commands](\COMMANDS.md) in any channel where the bot is present.
- Your messages will be displayed in the terminal as: `[channel] user: "message"`.

**Note:** Keep the terminal open to keep the bot running. To stop the bot, simply close the terminal.