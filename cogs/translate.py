import discord
from discord.ext import commands
from discord import app_commands
import aiohttp
try:
    from langdetect import detect, DetectorFactory
    DetectorFactory.seed = 0
    LANGDETECT_AVAILABLE = True
except ImportError:
    LANGDETECT_AVAILABLE = False

# Language codes for easy reference
LANGUAGES = {
    "english": "en",
    "spanish": "es",
    "french": "fr",
    "german": "de",
    "italian": "it",
    "portuguese": "pt",
    "russian": "ru",
    "japanese": "ja",
    "korean": "ko",
    "chinese": "zh",
    "arabic": "ar",
    "hindi": "hi",
    "turkish": "tr",
    "polish": "pl",
    "dutch": "nl",
    "swedish": "sv",
    "greek": "el",
    "czech": "cs",
    "thai": "th",
    "vietnamese": "vi",
}

# Reverse mapping: language code to language name
CODE_TO_LANGUAGE = {v: k for k, v in LANGUAGES.items()}

class Translate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="translate_to_english",
        description="Auto-detect language and translate to English"
    )
    @app_commands.describe(text="Text to translate to English")
    async def translate_to_english(
        self,
        interaction: discord.Interaction,
        text: str
    ):
        await interaction.response.defer(thinking=True)
        
        try:
            if not LANGDETECT_AVAILABLE:
                await interaction.followup.send(
                    "❌ Language detection library not installed. "
                    "Install it with: `pip install langdetect`"
                )
                return
            
            # Detect the language
            detected_lang_code = detect(text)
            detected_lang_name = CODE_TO_LANGUAGE.get(detected_lang_code, detected_lang_code.upper())
            
            # If already English, no need to translate
            if detected_lang_code == "en":
                await interaction.followup.send(
                    f"📝 Text is already in **English**:\n```{text}```"
                )
                return
            
            async with aiohttp.ClientSession() as session:
                url = "https://api.mymemory.translated.net/get"
                params = {
                    "q": text,
                    "langpair": f"{detected_lang_code}|en"
                }
                
                async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        
                        if data.get("responseStatus") == 200:
                            translated = data["responseData"]["translatedText"]
                            
                            embed = discord.Embed(
                                title="🌍 Auto-Translate to English",
                                color=discord.Color.blurple()
                            )
                            embed.add_field(
                                name=f"📝 {detected_lang_name.title()} (Detected)",
                                value=f"```{text}```",
                                inline=False
                            )
                            embed.add_field(
                                name="✅ English",
                                value=f"```{translated}```",
                                inline=False
                            )
                            embed.set_footer(text=f"Detected language: {detected_lang_name.title()}")
                            
                            await interaction.followup.send(embed=embed)
                        else:
                            await interaction.followup.send("❌ Translation failed.")
                    else:
                        await interaction.followup.send("❌ API error. Try again later.")
                        
        except Exception as e:
            await interaction.followup.send(f"❌ Error: {str(e)[:100]}")

async def setup(bot):
    await bot.add_cog(Translate(bot))
