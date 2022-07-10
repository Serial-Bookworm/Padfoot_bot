from botutils.constants import HS_API_URL_FIC_BLACKLIST, HS_API_URL_FIC_BLACKLIST_ADD_OR_MODIFY, FFN_CHECK_STR, AO3_CHECK_STR
import discord
import re
from discord.ext.commands import command, Cog
import asyncio
import requests
import json

from botutils.searchforlinks import get_ffn_url_from_query, get_ao3_url_from_query
from botutils.embeds import get_blacklist_embed
from botutils.utils import get_reply_message_for_fic_blacklist

class FicBlacklistCog(Cog):
    def __init__(self, bot):
        self.bot = bot


    @command('bl')
    async def blacklist_get(self, ctx):
        async with ctx.typing():
            await asyncio.sleep(1)
        try:
            response = requests.get(f'{HS_API_URL_FIC_BLACKLIST}')
            data = json.loads(response.text)

            embed_to_send = get_blacklist_embed(data)
            await ctx.send(embed=embed_to_send)
        except Exception as e:
            print(f"Exception occured: {e}")
            print(response.text)

    @command('bladd')
    async def blacklist_add(self, ctx):
        async with ctx.typing():
            await asyncio.sleep(1)
        
        query = ctx.message.content
        query = query[query.index('.bladd')+6: ]
        
        # extract link
        all_links = re.findall(r'(https?://[^\s]+)', query)
        if len(all_links) > 0:
            print('Found: ', all_links)
            for link in all_links:
                # get story_id
                if FFN_CHECK_STR in link:
                    try:
                        story_id = "FFN" + link[link.index('s/')+2 : link.index('/', link.index('s/')+4)]
                    except:
                        story_id = "FFN" + link[link.index('s/')+2 :]
                elif AO3_CHECK_STR in link:
                    try:
                        story_id = "AO3" + link[link.index('works/')+len('works/') : link.index('/', link.index('works/')+6)]
                    except:
                        story_id = "AO3" + link[link.index('works/')+len('works/') :]
                else:
                    return
                
                # send request to API for fic creation or vote modification 
                response = requests.get(f'{HS_API_URL_FIC_BLACKLIST_ADD_OR_MODIFY}/{story_id}')
                data = json.loads(response.text)
                response_to_send = get_reply_message_for_fic_blacklist(data)
                if response:
                    await ctx.send(response_to_send)
                else:
                    print("Server error.", data)
        elif query:
            query = query.strip()
            print('Query: ', query)
            try:
                story_id = int(query)
                primary_key_id = "ID" + str(story_id)
                # send request to API for vote addition 
                response = requests.get(f'{HS_API_URL_FIC_BLACKLIST_ADD_OR_MODIFY}/{primary_key_id}')
                data = json.loads(response.text)
                response_to_send = get_reply_message_for_fic_blacklist(data)
                if response:
                    await ctx.send(response_to_send)
            except Exception as e:
                await ctx.send("The fic index is not valid.")
                print(e)





def setup(bot):
    bot.add_cog(FicBlacklistCog(bot))
