import discord
from discord.ext import commands

from main import bot


class CommandesBasiques(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("CommandesBasiques loaded")

    # Commande pour générer le lien d'invitation du serveur
    @commands.command()
    async def invit(self, ctx):
        await ctx.channel.purge(limit=1)
        embed = discord.Embed(title="Lien d'invitation", color=0x00ff00)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url="https://emoji.gg/assets/emoji/5706-badly-drawn-invite-icon.png")
        embed.add_field(name="Le lien d'invitation a donné à tes amis est le suivant :",
                        value="https://discord.gg/WYPQ8thCdV", inline=True)

        await ctx.send(embed=embed)

    # Commande pour que le Bot repette le texte entré après le !perroquet
    @commands.command()
    async def perroquet(self, ctx, *texte):
        await ctx.send(" ".join(texte))

    # Commande pour avoir les infos du serveur ou le Bot est installé
    @commands.command()
    async def InfoServeur(self, ctx):
        await ctx.channel.purge(limit=1)
        server = ctx.guild
        numberOfTextChannels = len(server.text_channels)
        numberOfVoiceChannels = len(server.voice_channels)
        serverDescription = server.description
        numberOfUser = server.member_count
        serverName = server.name
        embed = discord.Embed(title="**Infos Serveur**", description=serverDescription,
                              url="http://libertalia.cluster1.easy-hebergement.net/", color=0x005eff)  # Lien pour que le titre soit au format texte clicable
        embed.set_author(name=serverName)
        embed.set_thumbnail(url="https://emoji.gg/assets/emoji/1214-discord.png")  # Lien de l'image pour l'embed
        embed.add_field(name="Le nombre d'utilisateurs est :", value=numberOfUser, inline=True)
        embed.add_field(name="Le nombre de salon textuel est :", value=str(numberOfTextChannels), inline=False)
        embed.add_field(name="Le nombre de salon vocaux est :", value=str(numberOfVoiceChannels), inline=False)
        # embed.add_field(name="Modérateur", value= ctx.author.name, inline=True)

        await ctx.send(embed=embed)
        # message = f"Le serveur **{serverName}** à un total de *{numberOfUser} utilisateurs*.\nLa description du
        # serveur est {serverDescription}. \nCe serveur possède {numberOfTextChannels} salons textuel ainsi que {
        # numberOfVoiceChannels} vocaux." await ctx.send(message)

    # Commande de rapport de Bug
    @commands.command()
    async def bug(self, ctx, desc=None, rep=None):
        await ctx.channel.purge(limit=1)
        user = ctx.author
        await ctx.author.send(
            '```Veuillez nous indiquer le bug que vous rencontrer (description courte). ```')
        responseplat = await bot.wait_for('message', check=lambda message: message.author == ctx.author,
                                          timeout=300)
        plateforme = responseplat.content
        await ctx.author.send('```Merci de bien vouloir nous expliquer plus en détail le bug que vous rencontrez.```')
        responseDesc = await bot.wait_for('message', check=lambda message: message.author == ctx.author,
                                          timeout=300)
        description = responseDesc.content
        await ctx.author.send('```Veuillez fournir un lien vers des photos/vidéos de ce bug.```')
        responseRep = await bot.wait_for('message', check=lambda message: message.author == ctx.author, timeout=300)
        replicate = responseRep.content
        await user.send('```Merci, un rapport de bug a été envoyé aux membres du staff. En cas de besoin, ils reviendront vers vous.```')
        embed = discord.Embed(title='Rapport de bug', color=0x00ff00)
        embed.add_field(name='Plateforme', value=plateforme, inline=True)
        embed.add_field(name='Reporté par', value=user, inline=True)
        embed.add_field(name='Description', value=description, inline=False)
        embed.add_field(name='Fichiers joints :', value="Voir ci-dessous", inline=True)

        adminBug = bot.get_channel(1019589443667111996)  # ID du channel ou le rapport sera envoyez
        await adminBug.send(embed=embed)
        await adminBug.send(replicate)


def setup(bot):
    bot.add_cog(CommandesBasiques(bot))