import asyncio
import random
import os

import discord
from discord.ext import commands
from imgurpython import ImgurClient


if os.getenv('LIVE') is not None:
    imgur_client_id = os.getenv('imgur-id')
    imgur_client_secret = os.getenv('imgur-secret')
    discord_token = os.getenv('discord-token')
    db = os.getenv('MONGODB_URI')
    if not discord.opus.is_loaded():
        discord.opus.load_opus('opus/lib/libopus.so')
else:
    import settings
    imgur_client_id = settings.imgur_client_id 
    imgur_client_secret = settings.imgur_client_secret
    discord_token = settings.discord_token
    db = None

    if not discord.opus.is_loaded():
        """ the 'opus' library here is opus.dll on windows
            or libopus.so on linux in the current directory
            you should replace this with the location the
            opus library is located in and with the proper filename.
            note that on windows this DLL is automatically provided for you
        """
    discord.opus.load_opus('opus')


description = '''Epic bot for messing around in discord.'''
bot = commands.Bot(command_prefix='/', description=description)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command(pass_context=True, description='AND HIS NAME IS: JOHN CENA!')
async def cena(ctx):
    """ JOHN CENA """
    channel = ctx.message.author.voice_channel
    if channel is None:
        await bot.say('Mee kanavalle, spede.')
    else:
        try:
            voice = await bot.join_voice_channel(channel)
            player = await voice.create_ytdl_player('https://www.youtube.com/watch?v=9EPL_4HyCFQ')
            player.volume = 0.05
            player.start()
            while not player.is_done():
                await asyncio.sleep(1)
            player.stop()
            await voice.disconnect()
        except discord.errors.ClientException:
            bot.say("Botilla on kiire spämmätä muualle")


@bot.command(pass_context=True, description='No mietippä?')
async def think(ctx):
    """ Makes you think :thinking_face: """
    channel = ctx.message.author.voice_channel
    if channel is None:
        await bot.say('Mee kanavalle, spede.')
    else:
        try:
            voice = await bot.join_voice_channel(channel)
            player = await voice.create_ytdl_player('https://www.youtube.com/watch?v=mxKDew6ldKY')
            player.volume = 0.05
            player.start()
            while not player.is_done():
                await asyncio.sleep(1)
            player.stop()
            await voice.disconnect()
        except discord.errors.ClientException:
            bot.say("Botilla on kiire spämmätä muualle")


@bot.command(description='Hassuja kissakuvia')
async def imgur(*search_terms):
    """ Fetches images from Imgur based on given arguments.
        Support single and multiple arguments"
    """
    client = ImgurClient(imgur_client_id, imgur_client_secret)

    search_terms = " ".join(search_terms)
    images = client.gallery_search(search_terms)
    if images:
        image = random.choice(images)
        if image.is_album == True:
            await bot.say(client.get_image(image.cover).link)
        else:
            await bot.say(image.link)
    else:
        await bot.say("Ei löytynyt kuvia termillä " + search_terms)


if __name__ == "__main__":
    try:
        bot.run(discord_token)
    except KeyboardInterrupt:
        print("Closing")
