import discord
from discord.ext import commands
from discord import app_commands
import aiohttp
import asyncio
import json

class ChatGPT(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_key = self.load_api_key()

    def load_api_key(self):
        try:
            with open("config.json", "r") as f:
                config = json.load(f)
                return config.get("groq_api_key", "")
        except:
            return ""

    @app_commands.command(name="chatgpt", description="Ask ChatGPT a question")
    async def chatgpt(self, interaction: discord.Interaction, prompt: str):
        await interaction.response.defer()
        
        if not self.api_key:
            await interaction.followup.send("❌ Groq API key not configured.")
            return

        api = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "llama3.1-70b-versatile",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 2000
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(api, json=payload, headers=headers, timeout=aiohttp.ClientTimeout(total=30)) as resp:
                    if resp.status != 200:
                        error_data = await resp.json()
                        error_msg = error_data.get("error", {}).get("message", "Unknown error")
                        await interaction.followup.send(f"❌ API Error: {error_msg}")
                        return
                    data = await resp.json()

            reply = data["choices"][0]["message"]["content"]
            
            # Split long responses into multiple messages if needed
            if len(reply) > 2000:
                messages = [reply[i:i+2000] for i in range(0, len(reply), 2000)]
                await interaction.followup.send(f"🤖 **AI Response:**\n{messages[0]}")
                for msg in messages[1:]:
                    await interaction.followup.send(msg)
            else:
                await interaction.followup.send(f"🤖 **AI Response:**\n{reply}")
        except asyncio.TimeoutError:
            await interaction.followup.send("⏱️ Request timed out. Try again later.")
        except aiohttp.ClientConnectorError as e:
            await interaction.followup.send(f"❌ Connection Error: Unable to reach Groq API. Check your internet connection.")
        except Exception as e:
            await interaction.followup.send(f"❌ Error: {str(e)}")

async def setup(bot):
    await bot.add_cog(ChatGPT(bot))
