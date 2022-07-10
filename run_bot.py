import discord
from discord.utils import get
from discord.ext.commands import Bot
import re
from bs4 import BeautifulSoup
import requests
import os
import time
import asyncio
from datetime import datetime
from dateutil.relativedelta import relativedelta
from discord import Embed, Colour
from discord.ext import commands, tasks
from dotenv import load_dotenv
from itertools import cycle

from botutils.constants import *
from brain import receiver

load_dotenv()  

TOKEN = os.environ.get('DISCORD_TOKEN')

intents = discord.Intents.all()
bot = Bot(command_prefix='.', help_command=None, intents=intents)

STATUSES = cycle(STATUS_ACTIVITY_DICT.keys())
ACTIVITIES = cycle(STATUS_ACTIVITY_DICT.values())

@tasks.loop(seconds=1)
async def loop_bot_status():
    """
    Loop through all statuses for the bot every 13 sec
    """

    await bot.wait_until_ready()

    await bot.change_presence(
        activity=discord.Activity(
            type=next(ACTIVITIES),
            name=(next(STATUSES)).strip()
        )
    )
    await asyncio.sleep(13)



@bot.event
async def on_message(message):
    """ Command to search and find the fanfiction by searching on google
    """
    
    # To see if commnds need to be executed too
    await bot.process_commands(message)
    
    # get the message 
    msg = message.content.lower()

    # Do not reply to self
    if message.author == bot.user:
        return  
    # Do not reply to any other bot
    if message.author.bot:
        return 
    
    # don't reply to a .noreply message
    if ".noreply" in msg:
        return
    
    # don't reply with fic embed to blacklist command
    if ".bl" in msg:
        return

    # see if message has any links or not
    embeds_to_send = receiver.process_message(msg)
    if embeds_to_send:
        async with message.channel.typing():
            for embed in embeds_to_send:
                try:
                    await message.reply(embed=embed, mention_author=False)
                except:
                    await message.reply(embed=embed)
    
@bot.event
async def on_member_join(member):
    if member.guild.id == 685366333319151636:
        channel = bot.get_channel(685382876442656961) # entrance-hall channel
        embed=discord.Embed(title=f"Welcome {member.name}!", description=f"Welcome to your first term at {member.guild.name}! We are glad to have you with us! 😀 \n\n 1. By joining us, you are agreeing with the Discord Age requirement (16+) to participate in all tasks of the server. If you are not of age, please enter once you are. \n\n 2. You cannot see everything, but that is because several rooms (channels) will only open themselves to you once you partake in the Sorting Ceremony (selecting a House and claiming your roles) in <#685387513937920020>. This is necessary to do in order to see restricted channels such as the HHr+ channels. \n\n 3. Mr. Filch has let out a list of what is allowed and forbidden in <#685382701729054916>  (the rules of the server). \n\n 4. If you are struggling to navigate in the server, you must solemnly swear that you are up to no good and open <#894947843465420810> . \n\n 5. Most importantly, we wish you a good term and do not forget to have fun, <#685366333319151649>  is a good place to start this task. \n\n Start chatting with the fam in the <#685366333319151649> !") # F-Strings!
        embed.set_thumbnail(url=member.avatar_url) # Set the embed's thumbnail to the member's avatar image!
        await channel.send(embed=embed)



# -----------------------------THE API STUFF GOES BELOW -------------------------------------------------------

from threading import Thread

import uvicorn
from fastapi import FastAPI 

app = FastAPI()

@app.get("/")
def main():
    return "The bot is alive!"

# run the bot as a FastAPI async func
@app.on_event("startup")
async def run():
    """to run the bot as a FastAPI async func"""

    try:
        loop_bot_status.start()
        bot.load_extension("helpercogs.help_cog")
        bot.load_extension("helpercogs.gsearch_cog")
        bot.load_extension("helpercogs.admin_cog")
        bot.load_extension("helpercogs.fic_blacklist")
        bot.load_extension("helpercogs.ffn_au_profile_cog")
        asyncio.create_task(bot.start(TOKEN))
    except:
        await bot.logout()
