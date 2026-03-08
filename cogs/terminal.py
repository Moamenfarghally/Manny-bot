"""
Terminal message sender cog for Discord bot
Allows sending messages to Discord channels from Python terminal
"""
import discord
from discord.ext import commands
import asyncio


class TerminalSender(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.terminal_task = None
    
    async def cog_load(self):
        """Start terminal handler when cog loads"""
        self.terminal_task = asyncio.create_task(self.terminal_message_handler())
    
    async def cog_unload(self):
        """Stop terminal handler when cog unloads"""
        if self.terminal_task:
            self.terminal_task.cancel()
    
    async def terminal_message_handler(self):
        """
        Handles terminal input to send messages to Discord channels
        """
        await self.bot.wait_until_ready()
        await asyncio.sleep(1)  # Wait for bot to fully initialize
        
        print("\n" + "="*50)
        print("TERMINAL MESSAGE SENDER ACTIVE")
        print("="*50)
        print("Format: channel_id message")
        print("DM Format: dm user_id message")
        print("Example: 1234567890 Hello World!")
        print("DM Example: dm 9876543210 Hi there!")
        print("Type 'help' for more info")
        print("="*50 + "\n")
        import sys
        sys.stdout.flush()
        
        loop = asyncio.get_event_loop()
        
        while not self.bot.is_closed():
            try:
                import sys
                sys.stdout.flush()
                user_input = await loop.run_in_executor(None, input, "Enter (channel_id message or dm user_id message): ")
                
                if user_input.lower() == 'help':
                    print("\nCommands:")
                    print("  channel_id message - Send message to channel")
                    print("  channel_id message_id message - Reply to message")
                    print("  channel_id message_id sticker:name - Reply with sticker")
                    print("  dm user_id message - Send DM to user")
                    print("  channels - List available channels")
                    print("  stickers - List available stickers")
                    print("  exit - Exit (bot will keep running)")
                    print()
                    continue
                
                if user_input.lower() == 'exit':
                    print("Exiting terminal sender...")
                    break
                
                # Check for DM command
                if user_input.lower().startswith("dm "):
                    parts = user_input[3:].split(" ", 1)  # Remove "dm " and split user_id and message
                    if len(parts) < 2:
                        print("❌ DM format: dm user_id message")
                        continue
                    try:
                        user_id = int(parts[0])
                    except ValueError:
                        print("❌ User ID must be a number")
                        continue
                    message_text = parts[1]
                    try:
                        user = await self.bot.fetch_user(user_id)
                        await user.send(message_text)
                        print(f"✅ DM sent to {user.name}!")
                    except discord.NotFound:
                        print(f"❌ User with ID {user_id} not found!")
                    except discord.Forbidden:
                        print(f"❌ Cannot send DM to {user_id} (user may have DMs disabled or bot blocked)")
                    except Exception as e:
                        print(f"❌ Error sending DM: {e}")
                    continue
                
                if user_input.lower() == 'channels':
                    print("\nAvailable channels:")
                    for guild in self.bot.guilds:
                        print(f"\n  Guild: {guild.name}")
                        for channel in guild.text_channels:
                            print(f"    - {channel.name} (ID: {channel.id})")
                    print()
                    continue
                
                if user_input.lower() == 'stickers':
                    print("\nAvailable stickers:")
                    for guild in self.bot.guilds:
                        if guild.stickers:
                            print(f"\n  Guild: {guild.name}")
                            for sticker in guild.stickers:
                                print(f"    - {sticker.name} (ID: {sticker.id})")
                    print()
                    continue
                
                # Parse input: "channel_id message" or "channel_id message_id message"
                parts = user_input.split(" ", 2)
                
                if len(parts) < 2:
                    print("❌ Invalid format! Use: channel_id message")
                    continue
                
                try:
                    channel_id = int(parts[0])
                except ValueError:
                    print("❌ First argument must be a channel ID (number)")
                    continue
                
                # Get channel
                channel = self.bot.get_channel(channel_id)
                if not channel:
                    print(f"❌ Channel with ID {channel_id} not found!")
                    continue
                
                # Check if second arg is a message ID or message text
                is_reply = False
                message_id = None
                message_text = None
                
                try:
                    message_id = int(parts[1])
                    is_reply = True
                    if len(parts) < 3:
                        print("❌ Reply format: channel_id message_id message")
                        continue
                    message_text = parts[2]
                except ValueError:
                    # Not a reply, parts[1] is the message text
                    message_text = " ".join(parts[1:])
                
                try:
                    if is_reply:
                        # Check if it's a sticker reply (format: sticker:name or sticker:id)
                        if message_text.startswith("sticker:"):
                            sticker_input = message_text[8:]  # Remove "sticker:" prefix
                            sticker_found = None
                            
                            # Get guild from channel for faster sticker search
                            guild = channel.guild
                            
                            # Try as ID first
                            try:
                                sticker_id = int(sticker_input)
                                for sticker in guild.stickers:
                                    if sticker.id == sticker_id:
                                        sticker_found = sticker
                                        break
                            except ValueError:
                                # Not an ID, search by name in guild stickers only
                                for sticker in guild.stickers:
                                    if sticker.name.lower() == sticker_input.lower():
                                        sticker_found = sticker
                                        break
                            
                            if not sticker_found:
                                print(f"❌ Sticker '{sticker_input}' not found in this guild! Use 'stickers' to list available stickers.")
                                continue
                            
                            # Reply with sticker
                            message = await channel.fetch_message(message_id)
                            await message.reply(sticker=sticker_found)
                            print(f"✅ Sticker reply sent to #{channel.name}!")
                        else:
                            # Reply with text
                            message = await channel.fetch_message(message_id)
                            await message.reply(message_text)
                            print(f"✅ Reply sent to #{channel.name}!")
                    else:
                        # Send normal message
                        await channel.send(message_text)
                        print(f"✅ Message sent to #{channel.name}!")
                except discord.NotFound:
                    print(f"❌ Message with ID {message_id} not found in #{channel.name}!")
                except discord.Forbidden:
                    print(f"❌ No permission to send messages in #{channel.name}")
                except Exception as e:
                    print(f"❌ Error: {e}")
            
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Error: {e}")
                await asyncio.sleep(0.1)


async def setup(bot):
    await bot.add_cog(TerminalSender(bot))
