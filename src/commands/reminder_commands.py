from discord.ext import commands
import asyncio

class ReminderCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reminders = {}

    async def send_reminder(self, user_id, channel_id, message):
        channel = self.bot.get_channel(int(channel_id))
        mention = f"<@{user_id}>"
        await channel.send(f"{mention} Reminder: {message}")

    async def send_reminder_delayed(self, delay, user_id, channel_id, message):
        await asyncio.sleep(delay)
        await self.send_reminder(user_id, channel_id, message)

    async def schedule_reminder(self, ctx, reminder_text):
        delay, message = self.parse_reminder(reminder_text)
        if delay is None:
            await ctx.send("Invalid reminder format.")
            return
        reminder_task = asyncio.create_task(self.send_reminder_delayed(delay, ctx.author.id, ctx.channel.id, message))
        self.reminders[reminder_task] = (ctx.author.id, ctx.channel.id, message)
        await ctx.send("Reminder scheduled.")

    def parse_reminder(self, reminder_text):
        try:
            parts = reminder_text.split()
            time_str = parts[0]
            unit = parts[1].lower()
            message = ' '.join(parts[2:])

            if unit == 'seconds' or unit == 'second' or unit == 'sec' or unit == 's':
                delay = int(time_str)
            elif unit == 'minutes' or unit == 'minute' or unit == 'min' or unit == 'm':
                delay = int(time_str) * 60
            elif unit == 'hours' or unit == 'hour' or unit == 'hr' or unit == 'h':
                delay = int(time_str) * 3600
            else:
                return None, None
            return delay, message
        except (ValueError, IndexError):
            return None, None

def setup(bot):
    bot.add_cog(ReminderCommands(bot))