# github.com/Ernestlph/Discord_Language_Bot/main.py

import discord
from discord.ext import commands
from discord import Intents
from collections import defaultdict
from asyncio import Lock, sleep

lock = Lock()

# Wrap your command functions with this
async def commandeering_bot(coro):
    global lock
    async with lock:
        await coro

# Initialise an instance of Intents.default() for default intents
intents = Intents.default()
intents.dm_messages = True
intents.message_content = True

# Then pass it to your bot
bot = commands.Bot(command_prefix='!', intents=intents, case_insensitive=True)


# Load token
with open("Token/token.txt", "r") as token_file:
    TOKEN = token_file.read().strip()


# Load commands

class UserState:
    CHOOSING_LANGUAGE = 1
    CHOOSING_LEVEL = 2
    CHOOSING_LESSON = 3

# Keep track of each user's state and chosen language.
user_states = defaultdict(lambda: {"state": UserState.CHOOSING_LANGUAGE, "chosen_language": None, "chosen_level": None, "chosen_lesson": None})


@bot.command(name='Start')
async def start(ctx):
    await commandeering_bot(_start(ctx))
free_bot_task = None

@bot.command(name='Stop')
async def Stop(ctx):
    if ctx.voice_client:
        ctx.voice_client.stop()
        await ctx.voice_client.disconnect()
    global free_bot_task
    if free_bot_task and not free_bot_task.cancelled():
        free_bot_task.cancel()

async def free_bot():
    await sleep(60)
    if lock.locked():
        lock.release()

@bot.command(name='Japanese')
async def Japanese(ctx):
    if user_states[ctx.author.id]["state"] == UserState.CHOOSING_LANGUAGE:
        user_states[ctx.author.id] = {
            "state": UserState.CHOOSING_LEVEL,
            "chosen_language": "Japanese",
            "chosen_level": None,
            "chosen_lesson": None,
        }
        await ctx.send('Ah, Japanese! Now choose your level with !Level1, !Level2, or !Level3.')
    else:
        await ctx.send("I'm afraid this command is out of context right now.")

@bot.command(name='Mandarin')
async def Mandarin(ctx):
    if user_states[ctx.author.id]["state"] == UserState.CHOOSING_LANGUAGE:
        user_states[ctx.author.id] = {
            "state": UserState.CHOOSING_LEVEL,
            "chosen_language": "Mandarin",
            "chosen_level": None,
            "chosen_lesson": None,
        }
        await ctx.send('Ah, Mandarin! Now choose your level with !Level1, !Level2, or !Level3.')
    else:
        await ctx.send("I'm afraid this command is out of context right now.")

@bot.command(name='Level1')
async def Level1(ctx):
    if user_states[ctx.author.id]["state"] == UserState.CHOOSING_LEVEL:
        user_states[ctx.author.id]["state"] = UserState.CHOOSING_LESSON
        user_states[ctx.author.id]["chosen_level"] = "Level1"
        if user_states[ctx.author.id]["chosen_language"] == "Japanese":
            await ctx.send('Starting at the base with Japanese, I see...Now choose your lesson with !Lesson 1 through !Lesson 30.')
        if user_states[ctx.author.id]["chosen_language"] == "Mandarin":
            await ctx.send('Starting at the base with Mandarin, I see...Now choose your lesson with !Lesson 1 through !Lesson 30.')
    else:
        await ctx.send("I'm afraid this command is out of context right now.")

@bot.command(name='Level2')
async def Level2(ctx):
    if user_states[ctx.author.id]["state"] == UserState.CHOOSING_LEVEL:
        user_states[ctx.author.id]["state"] = UserState.CHOOSING_LESSON
        user_states[ctx.author.id]["chosen_level"] = "Level2"
        if user_states[ctx.author.id]["chosen_language"] == "Japanese":
            await ctx.send('Intermediate with Japanese, I see...Now choose your lesson with !Lesson 1 through !Lesson 30.')
        if user_states[ctx.author.id]["chosen_language"] == "Mandarin":
            await ctx.send('Intermediate with Mandarin, I see...Now choose your lesson with !Lesson 1 through !Lesson 30.')
    else:
        await ctx.send("I'm afraid this command is out of context right now.")

@bot.command(name='Level3')
async def Level3(ctx):
    if user_states[ctx.author.id]["state"] == UserState.CHOOSING_LEVEL:
        user_states[ctx.author.id]["state"] = UserState.CHOOSING_LESSON
        user_states[ctx.author.id]["chosen_level"] = "Level3"
        if user_states[ctx.author.id]["chosen_language"] == "Japanese":
            await ctx.send('Advanced with Japanese, I see...Now choose your lesson with !Lesson 1 through !Lesson 30.')
        if user_states[ctx.author.id]["chosen_language"] == "Mandarin":
            await ctx.send('Advanced with Mandarin, I see...Now choose your lesson with !Lesson 1 through !Lesson 30.')
    else:
        await ctx.send("I'm afraid this command is out of context right now.")

@bot.command(name='Level4')
async def Level4(ctx):
    if user_states[ctx.author.id]["state"] == UserState.CHOOSING_LEVEL:
        user_states[ctx.author.id]["state"] = UserState.CHOOSING_LESSON
        user_states[ctx.author.id]["chosen_level"] = "Level4"
        if user_states[ctx.author.id]["chosen_language"] == "Japanese":
            await ctx.send('Unfortunately Japanese module does not have Level 4, please choose another level')
            user_states[ctx.author.id]["state"] = UserState.CHOOSING_LEVEL
            user_states[ctx.author.id]["chosen_level"] = None
        if user_states[ctx.author.id]["chosen_language"] == "Mandarin":
            await ctx.send('Advanced with Mandarin, I see...Now choose your lesson with !Lesson 1 through !Lesson 30.')
    else:
        await ctx.send("I'm afraid this command is out of context right now.")

@bot.command(name='Level5')
async def Level5(ctx):
    if user_states[ctx.author.id]["state"] == UserState.CHOOSING_LEVEL:
        user_states[ctx.author.id]["state"] = UserState.CHOOSING_LESSON
        user_states[ctx.author.id]["chosen_level"] = "Level5"
        if user_states[ctx.author.id]["chosen_language"] == "Japanese":
            await ctx.send('Unfortunately Japanese module does not have Level 5, please choose another level')
            user_states[ctx.author.id]["state"] = UserState.CHOOSING_LEVEL
            user_states[ctx.author.id]["chosen_level"] = None
        if user_states[ctx.author.id]["chosen_language"] == "Mandarin":
            await ctx.send('Advanced with Mandarin, I see...Now choose your lesson with !Lesson 1 through !Lesson 30.')
    else:
        await ctx.send("I'm afraid this command is out of context right now.")

async def play_lesson(ctx, lesson_number: int):
    if ctx.guild is None:
        await ctx.send('Please use this command within a server.')
        return

    global free_bot_task
    if free_bot_task:
        free_bot_task.cancel()
    
    voice_channel = ctx.voice_client.channel if ctx.voice_client else None
    channel = discord.utils.get(ctx.guild.channels, name='Language Lesson')

    if not voice_channel or voice_channel != channel:
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
        voice_channel = await channel.connect()

    audio_path = ""
    if user_states[ctx.author.id]["state"] == UserState.CHOOSING_LESSON:
        audio_path = f"file:/mnt/c/Discord_Bot/{user_states[ctx.author.id]['chosen_language']}/{user_states[ctx.author.id]['chosen_level']}/{user_states[ctx.author.id]['chosen_language']}{user_states[ctx.author.id]['chosen_level'][-1]}-Lesson{str(lesson_number).zfill(2)}"
        if (user_states[ctx.author.id]['chosen_language'] == "Mandarin") & (user_states[ctx.author.id]['chosen_level'] == ("Level1" or "Level2" or "Level3")):
            audio_path += ".flac"
        else:
            audio_path += ".mp3"
        
    audio_source = discord.FFmpegPCMAudio(audio_path)
    voice_channel.play(audio_source)
    free_bot_task = bot.loop.create_task(free_bot())

@bot.command(name='Lesson')
async def lesson(ctx, lesson_number: int):
    if 1 <= lesson_number <= 30:  # checks that the value is between 1 and 30
        await play_lesson(ctx, lesson_number)
    else:
        await ctx.send('I trust your resolve, but the lesson number should be between 1 and 30.')

async def _start(ctx):
    user_states[ctx.author.id] = {"state": UserState.CHOOSING_LANGUAGE, "chosen_language": None, "chosen_level": None, "chosen_lesson": None}

    free_bot_task = bot.loop.create_task(free_bot())
    await ctx.send('Greetings, ' + ctx.author.mention + '! Choose your path: !Japanese or !Mandarin')
                                          


bot.run(TOKEN)

