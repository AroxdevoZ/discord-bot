import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv(dotenv_path="config")

default_intents = discord.Intents.all()
default_intents.members = True
bot = commands.Bot(command_prefix="/", intents=default_intents)


@bot.event
async def on_ready():
    print("Ready !")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("La commande que vous avez entrée n'existe pas !")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Il manque un argument !")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("Vous n'avez pas les permissions pour exécuter cette commande !")
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send("Je suis désolé, mais je n'ai pas les permissions pour effectuer cette action !")


@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')


@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')


@bot.command()
async def relaod(ctx, extension):
    if extension:
        try:
            bot.reload_extension(f'cogs.{extension}')
        except:
            bot.load_extension(f'cogs.{extension}')


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(ENV['TOKEN'])


