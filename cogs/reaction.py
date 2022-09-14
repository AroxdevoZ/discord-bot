import discord
from discord.ext import commands

from main import bot


class reaction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("reaction loaded")

    # Commande de role automatique
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):  # auto roles
        message_id = payload.message_id
        membre = bot.get_guild(payload.guild_id).get_member(payload.user_id)
        if message_id == 844959797399781376:  # id du message reaction role
            guild_id = payload.guild_id
            guild = discord.utils.find(lambda g: g.id == guild_id, bot.guilds)

            if payload.emoji.name == 'Elyon':  # Nom de l'emoji
                role = discord.utils.get(guild.roles, name='Elyon')  # Nom du role
                # await membre.send(f"{membre} Tu obtiens le grade Elyon! sur le serveur **Libertalia**")
            elif payload.emoji.name == 'SOLO':
                role = discord.utils.get(guild.roles, name='SOLO')
                # await membre.send(f"{membre} Tu obtiens le grade SOLO! sur le serveur **Libertalia**")
            elif payload.emoji.name == 'coc':
                role = discord.utils.get(guild.roles, name='COC')
                # await membre.send(f"{membre} Tu obtiens le grade SOLO! sur le serveur **Libertalia**")
            else:
                role = discord.utils.get(guild.roles, name=payload.emoji.name)
            if role is not None:
                member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
                if member is not None:
                    await member.add_roles(role)
                    print("Grade ajouté !")
                else:
                    print("Le membre n'a pas été trouvé!")
            else:
                pass

        # Commande pour envoir de lien réseaux sociaux en Mp
        if message_id == 845251495296892968:  # id du message reaction role
            if payload.emoji.name == 'web':  # Nom de l'emoji
                await membre.send(
                    "Voici le lien du **Site** de libertalia :\n https://www.aroxdevoz.fr/libertalia/index.php") # lien vers le réseaux
            elif payload.emoji.name == 'facebook':
                await membre.send(
                    "Voici le lien de la page **Facebook** de libertalia :\n https://www.facebook.com/Libertalia-106158444978889")
            elif payload.emoji.name == 'facegroup':
                await membre.send(
                    "Voici le lien du **Groupe Facebook** de libertalia :\n https://www.facebook.com/groups/301822764942321")
            elif payload.emoji.name == 'twitter':
                await membre.send(
                    "Voici le lien de la page **Twitter** de Darlander :\n https://twitter.com/bkrlibertalia")
            elif payload.emoji.name == 'instagram':
                await membre.send(
                    "Voici le lien de la page **Instagram** de Darlander :\n https://www.instagram.com/bkr_libertalia/")
            elif payload.emoji.name == 'youtube':
                await membre.send(
                    "Voici le lien de la page **YouTube** de Darlander :\n https://www.youtube.com/channel/UCXBwVGCP5bRZruiN9MvNjVw")
            elif payload.emoji.name == 'twitch':
                await membre.send(
                    "Voici le lien de la page **Twitch** de Darlander :\n https://www.twitch.tv/lebeatertv")

        else:
            pass

    # Commande de retrai de role automatique
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        message_id = payload.message_id
        membre = bot.get_guild(payload.guild_id).get_member(payload.user_id)
        if message_id == 844959797399781376:  # id du message reaction role
            guild_id = payload.guild_id
            guild = discord.utils.find(lambda g: g.id == guild_id, bot.guilds)

            if payload.emoji.name == 'Elyon':  # Nom de l'emoji
                role = discord.utils.get(guild.roles, name='Elyon')  # Nom du role
                # await membre.send(f"{membre} Tu perds le grade Elyon! sur le serveur **Libertalia**")
            elif payload.emoji.name == 'SOLO':
                role = discord.utils.get(guild.roles, name='SOLO')
                # await membre.send(f"{membre} Tu perds le grade SOLO! sur le serveur **Libertalia**")
            else:
                role = discord.utils.get(guild.roles, name=payload.emoji.name)
            if role is not None:
                member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
                if member is not None:
                    await member.remove_roles(role)
                    print("Grade supprimé !")
                else:
                    print("Le membre n'a pas été trouvé!")
            else:
                print("Le role n'existe pas!")


def setup(bot):
    bot.add_cog(reaction(bot))