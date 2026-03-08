# bot.py
import discord
from discord.ext import commands, tasks
import os
import time
import json

def load_config():
    try:
        with open("config.json", "r") as f:
            return json.load(f)
    except:
        return {}

config = load_config()

intents = discord.Intents.default()
intents.message_content = True  # Required for !prefix commands


class MyBot(commands.Bot):
    def __init__(self):
        # Enable BOTH / and ! commands
        super().__init__(
            command_prefix=commands.when_mentioned_or("!", "/"),
            intents=intents
        )

        self.last_modified = {}

    async def setup_hook(self):
        # Load all cogs
        for file in os.listdir("./cogs"):
            if file.endswith(".py"):
                try:
                    await self.load_extension(f"cogs.{file[:-3]}")
                    print(f"Loaded cog: {file}")
                except Exception as e:
                    print(f"Failed to load {file}: {e}")

        # Sync slash commands
        await self.tree.sync()
        print("Slash commands synced.")

        # Start auto-reloader
        # self.watch_cogs.start()  # TEMPORARILY DISABLED

    async def on_ready(self):
        print(f"Bot logged in as {self.user}")

    # ---------------------------------------
    # AUTO RELOAD SYSTEM
    # ---------------------------------------
    @tasks.loop(seconds=1.5)
    async def watch_cogs(self):
        for file in os.listdir("./cogs"):
            if file.endswith(".py"):
                path = f"./cogs/{file}"
                last_edit = os.path.getmtime(path)

                # first-time tracking
                if file not in self.last_modified:
                    self.last_modified[file] = last_edit
                    continue

                # detect change
                if last_edit != self.last_modified[file]:
                    self.last_modified[file] = last_edit
                    try:
                        await self.reload_extension(f"cogs.{file[:-3]}")
                        print(f"♻️ Reloaded cog: {file}")

                        await self.tree.sync()
                        print("Slash commands synced.")

                    except Exception as e:
                        print(f"Error reloading {file}: {e}")

    @watch_cogs.before_loop
    async def before_watch(self):
        await self.wait_until_ready()


# Run bot
bot = MyBot()
TOKEN = config.get("bot_token", "")  # Load from config
if not TOKEN:
    print("❌ Bot token not found in config.json")
    exit(1)
bot.run(TOKEN)
