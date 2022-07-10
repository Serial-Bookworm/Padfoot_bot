import discord
import re
from discord.ext.commands import command, Cog
import asyncio

from botutils.searchforlinks import get_ffn_url_from_query, get_ao3_url_from_query
from brain.ffn_brain import ffn_searcher
from brain.ao3_brain import ao3_searcher

class GSearchCog(Cog):
    def __init__(self, bot):
        self.bot = bot


    @command('ff')
    async def ffsearch(self, ctx):
        async with ctx.typing():
            await asyncio.sleep(1)
        query = ctx.message.content
        query = query[query.index('.ff')+3: ]
        if query:
            link = get_ffn_url_from_query(query)
        if link:
            ffn_obj = ffn_searcher.FFnSearcher(' ') 
            ffn_obj.all_links_to_get_stories_for.append(link)
            ffn_obj.get_metadata()
            ffn_obj.fetch_ffn_embeds()
            embeds_to_send = ffn_obj.res_embeds
            if embeds_to_send:
                message = await ctx.send(embed=embeds_to_send[0])


    @command('ao3')
    async def ao3search(self, ctx):
        async with ctx.typing():
            await asyncio.sleep(1)
        query = ctx.message.content
        query = query[query.index('.ao3')+4: ]
        if query:
            link = get_ao3_url_from_query(query)
        if link:
            ao3_obj = ao3_searcher.Ao3Searcher(' ')
            ao3_obj.all_links_to_get_stories_for.append(link)
            ao3_obj.get_metadata()
            ao3_obj.fetch_ao3_embeds()
            embeds_to_send = ao3_obj.res_embeds
            if embeds_to_send:
                message = await ctx.send(embed=embeds_to_send[0])

        

def setup(bot):
    bot.add_cog(GSearchCog(bot))
