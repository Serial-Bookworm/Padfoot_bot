from os import link
from pydoc import describe
from turtle import title
from discord import Embed, Colour, embeds
from botutils.constants import DOCS_URL, HONEYSUCKLE_SUPPORT_SERVER_URL, ALL_METADATA_KEYS

def get_help_embed():
    """to return help embed
    """
    embed = Embed(
            title="How to use the Padfoot bot",
            description="v1.1.3",
            color=0xDB6F77
        )

    embed.add_field(
        name="Simple linking of stories",
        value="Just mention any FFN or AO3 story link in your message to get the bot's response.",
        inline=False
    )

    embed.add_field(
        name="Ffnet fics can be posted without their URLs via:",
        value="`.ff [fic name]` \
        \n **Example:**\n`.ff the lost horcrux`",
        inline=False
    )
    
    embed.add_field(
        name="AO3 fics can be posted without their URLs via:",
        value="`.ao3 [fic name]` \
        \n **Like:**\n`.ao3 from ruin`",
        inline=False
    )

    embed.add_field(
        name="FFN or AO3 author profiles can be displayed via:",
        value="`.au [author profile link]` \
        \n **Like:**\n`.au https://archiveofourown.org/users/GraeFoxx/pseuds/GraeFoxx`",
        inline=False
    )


    return embed

    

def get_about_embed():
    """to return about embed about hs bot from ffn
    """
    embed = Embed(
                title="About Padfoot bot v1.1.3",
                description="Built by **inPursuitOfMagic** for the Happy Harmony Homestead discord server and beyond.",
                        color=0xDB6F77
    )

    return embed


def get_embeds_ffn(list_of_dicts_of_metadata):
    """
    to get embeds list from list of dicts of story metadata
    """
    embeds_list = []
    for data in list_of_dicts_of_metadata:
        if data == "Not found.":
            continue
        embed = Embed(
            title= data['title'],
            url= data['link'],
            description= data['summary'],
            colour=Colour(0xDB6F77)
        )
        embed.set_author(name=data['author_name'])

        # add fields one by one
        if data['status'] == 'Complete':
            embed.add_field(
            name = 'Status',
            value = data['status'], 
            inline=True)
        else:
            embed.add_field(
            name = 'Last Updated:',
            value = data['updated'], 
            inline=True)
        
        embed.add_field(
            name='Length',
            value=str(data['num_chapters']) +
            " chapter(s) with "+str(data['num_words'])+" words", inline=True)

        if data['genres'] and not data['characters']:
            embed.add_field(name=f"Genres:", 
                        value=f"{data['genres']}", inline=False)
        elif data['characters'] and not data['genres']:
           embed.add_field(name=f"Genres:", 
                        value=f"{data['genres']}", inline=True)  
        else:
            embed.add_field(name=f"Genres:", 
                        value=f"{data['genres']}", inline=True)
            embed.add_field(name=f"Characters:",
                        value=str(data['characters']), inline=True)

        embed.add_field(name=f"Rated:",
                        value=f"{data['rated']}", inline=False)

        if data['thumb_image']:
            embed.set_thumbnail(
                url=f"https://www.fanfiction.net{data['thumb_image']}")
        
        embeds_list.append(embed)
    
    return embeds_list



def get_embeds_ao3(list_of_dicts_of_metadata):
    """
    to get embeds list from list of dicts of story metadata from ao3
    """
    embeds_list = []
    for data in list_of_dicts_of_metadata:
        embed = Embed(
            title= data['title'],
            url= data['link'],
            description= data['summary'],
            colour=Colour(0xDB6F77)
        )
        embed.set_author(name=data['authors'])

        embed.add_field(
            name = 'Status',
            value = data['status'], 
            inline=True)
        
        embed.add_field(
            name = 'Rating',
            value = data['rating'], 
            inline=True)
        
        embed.add_field(
            name = 'Language',
            value = data['language'], 
            inline=True)
        
        embed.add_field(
            name='Length',
            value=str(data['nchapters']) +
            " chapter(s) with "+str(data['words'])+" words", 
            inline=True)
        
        embed.add_field(
            name = 'Published',
            value = data['date_published'], 
            inline=True)

        if len(data['date_updated']) > 0:
            embed.add_field(
                name = 'Updated',
                value = data['date_updated'], 
                inline=True)

        if len(data['characters']) > 0:
            embed.add_field(
                name = 'Characters',
                value = data['characters'], 
                inline=True)
        
        if len(data['categories']) > 0:
            embed.add_field(
                name = 'Categories',
                value = data['categories'], 
                inline=True)

        if len(data['relationships']) > 0:
            embed.add_field(
                name = 'Relationships',
                value = data['relationships'], 
                inline=True)

        if len(data['warnings']) > 0:
            embed.add_field(
                name = 'Warnings',
                value = data['warnings'], 
                inline=True)

        stats = f"Kudos: {data['kudos']}, Bookmarks: {data['bookmarks']}"
        embed.add_field(
            name = 'Stats',
            value = stats, 
            inline=True)
                
        embeds_list.append(embed)
    
    return embeds_list


def get_embeds_portkey(list_of_dicts_of_metadata):
    """make and return portkey archive embeds for story metadata"""

    embeds_list = []
    for data in list_of_dicts_of_metadata:
        data = data["story"]
        sid = data["id"]
        embed = Embed(
            title= data['title'],
            url= f"https://www.portkey-archive.org/story/{sid}",
            description= data['summary'],
            colour=Colour(0xDB6F77)
        )
        embed.set_author(name=data['author']["name"])

        embed.add_field(
            name='Length',
            value=str(data['chapter_count']) +
            " chapter(s) with "+str(data['word_count'])+" words", 
            inline=True)

        embed.add_field(
            name = 'Status',
            value = data['status'], 
            inline=True)
        
        embed.add_field(
            name = 'Genres',
            value = ", ".join(data["genres"]), 
            inline=True)
        
        embed.add_field(
            name = 'Rating',
            value = data["rating"], 
            inline=True)

        embeds_list.append(embed)
        
    return embeds_list

        
        



def get_blacklist_embed(data):
    """to return an embed with all blacklisted fics with author, story, and votes count"""
    
    embed = Embed(
            title= "Blacklisted fics 💀",
            # url= data['link'], TODO: ADD URL OF BLACKLIST PAGE ON HHR WEBSITE
            description= "All blacklisted fics with vote count",
            colour=Colour(0xDB6F77)
        )
    for i, ficdict in enumerate(data):
        embed.add_field(
            name= f'Rank {i+1}: {ficdict["story_name"]} by {ficdict["author_name"]} with {ficdict["votes"]} votes.',
            value="\u200b",
            inline=False
        )
    
    return embed


def get_ffn_story_link_from_id(story_id):
    return f"https://fanfiction.net/s/{story_id}"


# AU Profile Embed Maker class

class FFNAUProfileEmbedMaker:
    def __init__(self, au_link, au_name, au_intro_line, au_names_ids_tuple, au_story_details) -> None:
        self.au_name = au_name
        self.au_link = au_link
        self.au_intro_line = au_intro_line
        self.au_names_ids_tuple = au_names_ids_tuple
        self.au_story_details = au_story_details

        self.page_limit = len(self.au_names_ids_tuple) // 5
    
    def get_page_limit(self):
        return self.page_limit

    def get_embed_page(self, page=1):
        """to return author profile embeds"""

        embed = Embed(
                title= f"Name: {self.au_name}",
                url= self.au_link,
                description= self.au_intro_line,
                colour=Colour(0xDB6F77)
            )
        start_story = (page-1) * 5
        for storynameid, storydetails in zip(self.au_names_ids_tuple[start_story:start_story+5], self.au_story_details[start_story:start_story+5]):
            link = get_ffn_story_link_from_id(storynameid[1])
            embed.add_field(
                    name= storynameid[0],
                    value= f"{storydetails}, [Link]({link})",
                    inline=False
            )   
        embed.set_footer(text=f"Page: {page}/{self.page_limit}") 

        return embed

def AO3AUProfileEmbedMaker(au_link_ao3, au_name_ao3, au_intro_line_ao3, au_story_details_ao3):
    """genereate embedds for author profile data from AO3"""

    embed = Embed(
            title= f"Name: {au_name_ao3}",
            url= au_link_ao3,
            description= au_intro_line_ao3,
            colour=Colour(0xDB6F77)
        )
    for work in au_story_details_ao3:
        embed.add_field(
            name = f"{work['title']} in {work['fandoms']} with {work['words']} words",
            value = work["summary"],
            inline = False
        )
    
    return embed


def embed_starboard_channel(message):
    """
    embed message to send in starboard channel
    """

    embed = Embed(
        description = f"{message.content}"
    )
    
    embed.set_author(name = message.author.name, icon_url=message.author.avatar_url)

    if len(message.attachments):
        for attachment in message.attachments:
            if attachment.content_type == "image/webp":
                embed.set_image(url=attachment.url)
                break
            else:
                embed.add_field(name="File(s) attached.", value="Jump to message to view.", inline=False)
    
    embed.add_field(
            name = f"Jump to message",
            value = f"[Link]({message.jump_url})",
            inline=False
        )

    embed.add_field(name = "Sent on: ", value = str(message.created_at)[:10], inline=False)

    return embed