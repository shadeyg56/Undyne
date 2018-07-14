import discord
from discord.ext import commands
import time
import asyncio
import os

bot = commands.Bot(command_prefix=commands.when_mentioned_or("@Undyne"))
bot.channels = [451119144021131284, 451119972362485780, 451119987856506902]
bot.purges = 0

@bot.event
async def on_ready():
  print('------------------------------------')
  print('THE BOT IS ONLINE')
  print('------------------------------------')
  print("Name: {}".format(bot.user.name))
  print('Author: shadeyg56')
  print("ID: {}".format(bot.user.id))
  print('DV: {}'.format(discord.__version__))
  bot_start = time.strftime("%X")
  await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="First purge at {} GMT+1".format(bot_start)))
  await asyncio.sleep(86400)
  bot.loop.create_task(auto_prune())


async def auto_prune():
	await bot.wait_until_ready()
	await asyncio.sleep(1)
	while not bot.loop.is_closed():
		current_time = time.strftime("%X")
		for channel in bot.channels:
			channel = bot.get_channel(channel)
			messages = await channel.history(limit=None).flatten()
			await channel.purge(limit=len(messages))
			await channel.send("Cleared last 400 messages from the last 24 hours. Next purge will be at {} GMT+1 at tomorrow if the bot isn't stopped.".format(current_time))
		print("Cleared last 400 from the last 24 hours. Next purge will be at {} GMT+1 at tomorrow if the bot isn't stopped.".format(current_time))
		bot.purges += 1 
		await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="Next purge at {} GMT+1 | Purges so far: {}".format(current_time, bot.purges)))
		await asyncio.sleep(86400)

@bot.command()
@commands.has_permissions(manage_messages=True)
async def force_purge(ctx):
	"Force the bot to purge the messages immediatly instead of waiting 24 hours."
	for channel in bot.channels:
			channel = bot.get_channel(channel)
			messages = await channel.history(limit=None).flatten()
			await channel.purge(limit=len(messages))
			await channel.send("Cleared last 400 messages forcefully. Timer is still going for next purge")
	print("Cleared last 400 messages forcefully. Timer is still going for next purge")
			

bot.run(os.get_environ("TOKEN"))
