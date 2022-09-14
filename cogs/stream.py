import discord
from discord import Streaming, Activity, activity
from discord.ext import commands
from discord.utils import get

from main import bot


class streaming(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Stream loaded")

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        role = get(after.guild.roles, name="ON AIR")
        channel = get(after.guild.channels, id=844925453471186964)

        try:
            activity_type = after.activity.type
            if activity_type is discord.ActivityType.streaming:
                await after.add_roles(role)
                await channel.send(
                    f"{before.mention} is streaming on {Streaming.twitch_name}: {Streaming.name}.\nJoin here: {Streaming.url}")
            elif activity_type is discord.ActivityType.streaming:
                await after.remove_roles(role)
            else:
                return
        except:
            pass


def setup(bot):
    bot.add_cog(streaming(bot))
