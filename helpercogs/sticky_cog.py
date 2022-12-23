from discord.ext.commands import Cog
from discord import Embed, Colour
from botutils.constants import HHR_PLUS_REC_ROOM_CHANNEL_ID, HHR_REC_ROOM_CHANNEL_ID

class StickyCog(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message):
        # Do not reply to self
        if message.author == self.bot.user:
            return  
        # Do not reply to any other bot
        if message.author.bot:
            return 
        if message.channel.id == HHR_REC_ROOM_CHANNEL_ID:
            with open('static/sticky_last_message_hhr_rec.txt', 'r') as f:
                last_message_id = f.read()
            if last_message_id:
                msg = await message.channel.fetch_message(last_message_id)
                await msg.delete()
            embed = Embed(
                title= "Please send only links to stories in this channel.",
                # url= data['link'], TODO: ADD URL OF BLACKLIST PAGE ON HHR WEBSITE
                description= "For more information, refer to the Marauder's map channel.",
                colour=Colour(0xDB6F77)
            )
            msg = await message.channel.send(embed=embed)
            with open('static/sticky_last_message_hhr_rec.txt', 'w') as f:
                f.write(str(msg.id))

        if message.channel.id == HHR_PLUS_REC_ROOM_CHANNEL_ID:
            with open('static/sticky_last_message_hhr_plus_rec.txt', 'r') as f:
                last_message_id = f.read()
            if last_message_id:
                msg = await message.channel.fetch_message(last_message_id)
                await msg.delete()
            embed = Embed(
                title= "Please send only links to stories in this channel.",
                # url= data['link'], TODO: ADD URL OF BLACKLIST PAGE ON HHR WEBSITE
                description= "For more information, refer to the Marauder's map channel.",
                colour=Colour(0xDB6F77)
            )
            msg = await message.channel.send(embed=embed)
            with open('static/sticky_last_message_hhr_plus_rec.txt', 'w') as f:
                f.write(msg.id)


def setup(bot):
    bot.add_cog(StickyCog(bot))