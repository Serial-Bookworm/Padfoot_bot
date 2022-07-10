from botutils.constants import AO3_AUTHOR_CHECK_STR, FFN_AUTHOR_CHECK_STR
from botutils.embeds import AO3AUProfileEmbedMaker, FFNAUProfileEmbedMaker
from brain.ao3_brain.ao3_au_profile import AO3AuProfiler
from brain.ffn_brain.ffn_au_profile import FFNAuProfiler
import re
from discord.ext.commands import command, Cog
import asyncio

class FFNAuProfileCog(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command('au')
    async def au_profile(self, ctx):
        async with ctx.typing():
            await asyncio.sleep(1)
        
        # get the message
        query = ctx.message.content
        query = query[query.index('.au')+3: ]
        # a flag to keep track of au links found or not
        au_links_found_ffn, au_links_found_ao3 = True, True

        # send it to both au profilers to extract bio and story details
        if FFN_AUTHOR_CHECK_STR in query:
            all_au_data_ffn = FFNAuProfiler(query)
            au_link_ffn, au_name_ffn, au_intro_line_ffn, au_names_ids_tuple_ffn, au_story_details_ffn = all_au_data_ffn.get_all_metadata_for_embed_generation()
            if not au_link_ffn or not au_name_ffn or not au_intro_line_ffn or not au_names_ids_tuple_ffn or not au_story_details_ffn:
                au_links_found_ffn = False
        else:
            au_links_found_ffn = False
        if  AO3_AUTHOR_CHECK_STR in query:
            all_au_data_ao3 = AO3AuProfiler(query)
            au_link_ao3, au_name_ao3, au_intro_line_ao3, au_story_details_ao3 = all_au_data_ao3.get_all_metadata_for_embed_generation()
            if not au_link_ao3 or not au_name_ao3 or not au_intro_line_ao3 or not au_story_details_ao3:
                au_links_found_ao3 = False
        else:
            au_links_found_ao3 = False

        # if no links were found in both ffn and ao3, nothing left to do here
        if not au_links_found_ao3 and not au_intro_line_ffn:
            return

        # get embeds from both
        if au_links_found_ffn:
            ffn_au_embedmaker_obj = FFNAUProfileEmbedMaker(au_link_ffn, au_name_ffn, au_intro_line_ffn, au_names_ids_tuple_ffn, au_story_details_ffn)
            embed_au = ffn_au_embedmaker_obj.get_embed_page() # get first page of embed
            message = await ctx.send(embed=embed_au)
            await message.add_reaction('✅') 
        # page_limit = ffn_au_embedmaker_obj.get_page_limit() # don't need this now as not using page system in embeds anymore
        if au_links_found_ao3:
            embed_au = AO3AUProfileEmbedMaker(au_link_ao3, au_name_ao3, au_intro_line_ao3, au_story_details_ao3)
            message = await ctx.send(embed=embed_au)
            await message.add_reaction('✅') 


def setup(bot):
    bot.add_cog(FFNAuProfileCog(bot))
