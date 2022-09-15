import asyncio
import aiofiles
import discord
import random
from discord.ext import commands

from main import bot

intents = discord.Intents.default()
intents.members = True
bot.warnings = {}
ban_list = []
day_list = []
server_list = []


class CommandesStaff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        for guild in bot.guilds:
            async with aiofiles.open(f"{guild.id}.txt", mode='a') as temp:
                pass

            bot.warnings[guild.id] = {}

            #for guild in bot.guilds:
                #async with aiofiles.open(f"{guild.id}.txt", mode="r") as file:
                    #lines = await file.readlines()

                    #for line in lines:
                        #data = line.split(" ")
                        #member_id = int(data[1])
                        #admin_id = int(data[2])
                        #reason = " ".join(data[2:]).strip("\n")

                        #try:
                            #bot.warnings[guild.id][member_id][1] += 1
                            #bot.warnings[guild.id][member_id][2].append((admin_id, reason))

                        #except KeyError:
                            #bot.warnings[guild.id][member_id] = [1, [(admin_id, reason)]]

        print("CommandersStaff loaded")

    # Commande de concour (geaveway)
    @commands.has_permissions(manage_messages=True)
    @commands.command()
    async def concours(self, ctx):
        await ctx.send("Le concours commancera dans 10 secondes. Evoyez \"moi\" dans ce channel pour y participer.")

        players = []

        def check(message):
            return message.channel == ctx.message.channel and message.author not in players and message.content == "moi"

        try:
            while True:
                participation = await bot.wait_for('message', timeout=10, check=check)
                players.append(participation.author)
                print("Nouveau participant : ")
                print(participation)
                await ctx.send(
                    f"**{participation.author.name}** ta participation au concours à bien été prise en compte! \nLe tirage commence dans 10 secondes")
        except:
            print("Demarrage du tirrage")

        gagner = ["nom de la recompense"]

        await ctx.send("Le tirage va commencer dans 3...")
        await asyncio.sleep(1)
        await ctx.send("2")
        await asyncio.sleep(1)
        await ctx.send("1")
        await asyncio.sleep(1)
        loser = random.choice(players)
        price = random.choice(gagner)
        await ctx.send(f"La personne qui à gagnée un {price} est ...")
        await asyncio.sleep(1)
        await ctx.send("**" + loser.name + "**" + " !")

    # Commande de suppresion de message (à amélioré)
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, nombre: int):
        messages = await ctx.channel.history(limit=nombre + 1).flatten()

        for message in messages:
            await message.delete()

    # Commande pour kick un membre du serveur
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.User, *reason):
        await ctx.channel.purge(limit=1)
        reason = " ".join(reason)
        await ctx.guild.kick(user, reason=reason)
        await ctx.send(f"{user} à été kick.")

    # Ceci est un processus d'arrière-plan pour le tempsban
    async def countdown(self):
        await bot.wait_until_ready()
        while not bot.is_closed:
            await asyncio.sleep(1)
            day_list[:] = [x - 1 for x in day_list]
            for day in day_list:
                if day <= 0:
                    try:
                        await bot.unban(server_list[day_list.index(day)], ban_list[day_list.index(day)])
                    except:
                        print('Error! User already unbanned!')
                    del ban_list[day_list.index(day)]
                    del server_list[day_list.index(day)]
                    del day_list[day_list.index(day)]

    # Command Pour ban temporairement un membre
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def tempban(self, ctx, member: discord.Member, days=1):
        if str(ctx.message.author.name):
            try:
                await bot.ban(member, delete_message_days=0)
                await bot.say('Utilisateur banni pour **' + str(days) + ' jour(s)**')
                ban_list.append(member)
                day_list.append(days * 24 * 60 * 60)
                server_list.append(ctx.message.server)
            except:
                await bot.say('Erreur! Utilisateur non actif')
        else:
            await bot.say("Vous n'êtes pas autorisé à bannir des utilisateurs!")

    # Commande pour ban un membre (à amélioré = tempban)
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.User, *, reason="Aucune raison n'a été donné"):
        await ctx.channel.purge(limit=1)
        await ctx.guild.ban(user, reason=reason)
        embed = discord.Embed(title="**Banissement**", description="Un membre a été ban !",
                              url="http://libertalia.cluster1.easy-hebergement.net/fr/reglement-de-la-communaute", color=0x005eff)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url="https://discordemoji.com/assets/emoji/BanneHammer.png")
        embed.add_field(name="Le Membre banni est :", value=user.name, inline=True)
        embed.add_field(name="La raison du ban est :", value=reason, inline=False)
        # embed.add_field(name="Modérateur", value= ctx.author.name, inline=True)

        ban = bot.get_channel(1019591239429005323)
        await ban.send(embed=embed)

    # Commande pour déban un membre (Ne fonctionne pas)
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user, *reason):
        await ctx.channel.purge(limit=1)
        reason = " ".join(reason)
        userName, userId = user.split("#")
        bannedUsers = await ctx.guild.bans()
        for i in bannedUsers:
            if i.user.name == userName and i.user.discriminator == userId:
                await ctx.guild.unban(i.user, reason=reason)
                await ctx.send(f"{user} à été unban.")
                return
        await ctx.send(f"L'utilisateur {user} n'a pas été trouvé.")

    # Commande pour avertir un membre (fonctionne mais n'affice pas le message dans le channel approprié et ne garde pas les warn en mémoire)
    #@commands.command()
    #@commands.has_permissions(administrator=True)
    #async def warn(self, ctx, member: discord.Member = None, *, reason=None):
        #await ctx.channel.purge(limit=1)
        #if member is None:
            #return await ctx.send("Le membre fourni n'a pas pu être trouvé ou vous avez oublié d'en fournir un.")

        #if reason is None:
            #return await ctx.send("Veuillez fournir une raison pour avertir cet utilisateur.")

        #try:
            #first_warning = False
            #bot.warnings[ctx.guild.id][member.id][0] += 1
            #bot.warnings[ctx.guild.id][member.id][1].append((ctx.author.id, reason))

        #except KeyError:
            #first_warning = True
            #bot.warnings[ctx.guild.id][member.id] = [1, [(ctx.author.id, reason)]]

        #count = bot.warnings[ctx.guild.id][member.id][0]

        #async with aiofiles.open(f"{ctx.guild.id}.txt", mode="a") as file:
            #await file.write(f"{member.id} {ctx.author.id} {reason}\n")
            
        #embed = discord.Embed(title="**Avertissement**", description="Un membre a été warn !",
                              #url="http://libertalia.cluster1.easy-hebergement.net/fr/reglement-de-la-communaute", color=0x005eff)
        #embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        #embed.set_thumbnail(url="https://cdn3.emoji.gg/emojis/2889-virus.png")
        #embed.add_field(name="Le Membre warn est :", value=user.name, inline=True)
        #embed.add_field(name="La raison du warn est :", value=reason, inline=False)

        #war = bot.get_channel(1019591863738564678)
        #await war.send(embed=embed)

    # Commande pour voir le nombre d'avertissement et les raisons de ce dernier pour un membre
    #@commands.command()
    #@commands.has_permissions(administrator=True)
    #async def warnings(self, ctx, member: discord.Member=None):
        #await ctx.channel.purge(limit=1)
        #if member is None:
            #return await ctx.send("Le membre fourni n'a pas pu être trouvé ou vous avez oublié d'en fournir un.")

        #embed = discord.Embed(title=f"Affichage d'avertissement pour {member.name}", description="", colour=discord.Color.red())
        #embed.set_thumbnail(url="https://emoji.gg/assets/emoji/Warning.png")
        #try:
            #i = 1
            #for admin_id, reason in bot.warnings[ctx.guild.id][member.id][1]:
                #admin = ctx.guild.get_member(admin_id)
                #embed.description += f"**Avertissement {i}** donné par: {admin.mention} **Pour la raison suivante:** *'{reason}'*.\n"
                #i += 1
            #warinfo = bot.get_channel(1019591863738564678)
            #await warinfo.send(embed=embed)

        #except KeyError:
            #await ctx.send("Cet utilisateur n'a aucun avertissement.")

    # Création du role Muted si pas présent sur le serveur
    async def createMutedRole(self, ctx):
        mutedRole = await ctx.guild.create_role(name="Muted",
                                                permissions=discord.Permissions(send_messages=False, speak=False),
                                                reason="Creation du role Muted.")
        for channel in ctx.guild.channels:
            await channel.set_permissions(mutedRole, send_messages=False, speak=False)
        return mutedRole

    async def getMutedRole(self, ctx):
        roles = ctx.guild.roles
        for role in roles:
            if role.name == "Muted":
                return role

        return await self.createMutedRole(ctx)

    # Commande pour Mute un membre
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, *, reason="Aucune raison n'a été renseigné"):
        await ctx.channel.purge(limit=1)
        mutedRole = await self.getMutedRole(ctx)
        await member.add_roles(mutedRole, reason=reason)
        await ctx.send(f"{member.mention} a été mute !")
        
    # Commande pour Mute temporairement un membre
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def tempmute(self, ctx, member: discord.Member, time):
        muted_role = await self.getMutedRole(ctx)
        time_convert = {"s": 1, "m": 600, "h": 36000, "d": 864000}
        tempmute = int(time[0]) * time_convert[time[-1]]
        await ctx.message.delete()
        await member.add_roles(muted_role)
        embed = discord.Embed(description=f"✅ **{member.display_name}#{member.discriminator} à été mute avec sucés** {time/60}.",
                              color=discord.Color.green())
        await ctx.send(embed=embed, delete_after=30)
        await asyncio.sleep(tempmute)
        await member.remove_roles(muted_role)

    # Commande pour démute un membre
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member, *, reason="Aucune raison n'a été renseigné"):
        await ctx.channel.purge(limit=1)
        mutedRole = await self.getMutedRole(ctx)
        await member.remove_roles(mutedRole, reason=reason)
        await ctx.send(f"{member.mention} à été unmute!")

    # Commande pour questionnaire (pour le moment 2 réponse à amélioré)
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def poll(self, ctx, *, question):
        await ctx.channel.purge(limit=1)
        message = await ctx.send(f"Nouveau sondage: \n**{question}** \n✅ = **Oui**\n❎ = **Non**")
        await message.add_reaction('✅')
        await message.add_reaction('❎')


def setup(bot):
    bot.add_cog(CommandesStaff(bot))
