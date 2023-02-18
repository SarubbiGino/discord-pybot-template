import discord
from discord.ext import commands
import datetime

client = discord.Client()

bot = commands.Bot(command_prefix='', description="This is a helper bot")

@bot.command()
async def comandos(ctx):
    embed = discord.Embed(title=f"{ctx.guild.name}",description="aqui va una lista de los comandos para que el bot responda",
    timestamp=datetime.datetime.utcnow(), color = discord.Color.blue())
    embed.set_thumbnail(url="https://www.clipartmax.com/png/middle/72-720707_imagenes-sin-fondo-renders-png-renders-sin-fondo.png")

    await ctx.send(embed=embed)
@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command(name='Saluda')
async def greet(ctx):
    await ctx.send('¡Hola!')

#Events


intent = discord.Intents.all()
bot.run('MTA3NTkwNjEwNTQxNjM1MTgxNQ.Gi9VPl.GgKLRE4hlVLXjltGA1cb4AxT1I-IAu-gLF2Kuo')