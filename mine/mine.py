import discord
from .utils import checks
import asyncio
from discord.ext import commands

class MinerCog:
    """Automine stuff"""

    def __init__(self, bot):
        self.bot = bot
        self.timers = []
        self.debugroom = self.bot.get_channel('425980791550377996')
        self.bank = self.bot.get_cog('Economy').bank
        self.masternodes = []

    async def mine():
        await asyncio.sleep(5000)
        for uid in self.timers:
            self.bank.deposit_credits(uid, 300 if uid in self.masternodes else 30)
            await self.bot.send_message(self.debugroom, "{} kapott penzt".format(uid))
            
    async def on_voice_state_update(self, before, after):
        await self.bot.send_message(self.debugroom,"room trigger")
        before_members = before.voice.voice_channel.voice_members
        after_members = after.voice.voice_channel.voice_members
        await self.bot.send_message(self.debugroom, "chage before"+ u.name for u in before_members)
        await self.bot.send_message(self.debugroom, "chage after"+ u.name for u in after_members)
        if(len(after_members) >= 3):
            if u"\U0001F4B0" not in after.voice.voice_channel.name:
                await self.bot.edit_channel(after.voice.voice_channel, name=after.voice.voice_channel.name+u"\U0001F4B0")
            for u in after_members:
                await self.bot.send_message(self.debugroom, "after members: {}".format(u.name))
                if u not in self.timers:
                    await self.bot.send_message(self.debugroom, "banyaszok {}-nak".format(u.name))
                    self.timers.append(u.id)
        if(len(before_members) < 3):            
            await self.bot.edit_channel(after.voice.voice_channel, name=after.voice.voice_channel.name.replace(u"\U0001F4B0", ''))
            for u in before_members:
                await self.bot.send_message(self.debugroom, "before members: {}".format(u.name))
                if u in self.timers:
                    await self.bot.send_message(self.debugroom, "{} nem banyaszik".format(u.name))
                    self.timers.remove(u.id)
                    
    @commands.command(pass_context=True)
    @checks.mod_or_permissions(administrator=True)
    async def addmasterminer(self, ctx, uid):
        if uid not in self.masternodes:
            self.masternodes.append(uid)
        else:
            await self.bot.send_message(ctx.message.channel, "{} mar masterminer!".format(uid))

    @commands.command(pass_context=True)
    @checks.mod_or_permissions(administrator=True)
    async def delmasterminer(self, ctx, uid):
        if uid in self.masternodes:
            self.masternodes.remove(uid)
        else:
            await self.bot.send_message(ctx.message.channel, "{} nem is masterminer!".format(uid))

    @commands.command(pass_context=True)
    @checks.mod_or_permissions(administrator=True)
    async def resetminers(self, ctx):
        self.timers = []
        self.masternodes = []
        await self.bot.send_message(ctx.message.channel, "Minerek visszaallitva")

    @commands.command(pass_context=True)
    @checks.mod_or_permissions(administrator=True)
    async def debugminers(self, ctx):
        await self.bot.send_message(ctx.message.channel, "minerek: " + str(self.timers))
        await self.bot.send_message(ctx.message.channel, "master minerek: " + str(self.masternodes))

def setup(bot):
    bot.add_cog(MinerCog(bot))
