from discord.ext import commands


class members(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("members loaded")

    # Commande de bienvenue lorsqu'un menbre rejoind le serveur (à amélioré graphiquement)
    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.get_channel(
            844926346765664308)  # id du channel pour annoncé qu'un membre est arrivé sur le serveur
        await channel.send(f"Acceuillons {member.mention} dans la meute. Bienvenue à toi.")

    # Commande quand un membre quitte le serveur
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = member.guild.get_channel(844926346765664308)  # id du channel pour annoncé qu'un membre nous à quittez
        await channel.send(f"{member.mention} nous a quittez.")


def setup(bot):
    bot.add_cog(members(bot))