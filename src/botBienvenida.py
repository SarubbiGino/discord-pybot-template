import json, os
from discord.ext import commands
import discord
from discord.ext.commands import has_any_role
import datetime
bott = commands.Bot(command_prefix='', description="This is a helper bot")

@bott.command()
async def comandos(ctx):
    embed = discord.Embed(title=f"{ctx.guild.name}",description="aqui va una lista de los comandos para que el bot responda",
    timestamp=datetime.datetime.utcnow(), color = discord.Color.blue())
    embed.set_thumbnail(url="https://www.clipartmax.com/png/middle/72-720707_imagenes-sin-fondo-renders-png-renders-sin-fondo.png")

    await ctx.send(embed=embed)

class Welcome_Embed():
	def __init__(self, member):
		# Member = nickname del nuevo usuario
		self.member = member


	@property
	def enviar(self):
		self.embed = discord.Embed(title=f"Hola {self.member}. Para unirte al servidor debes aceptar las siguientes reglas...", colour=int("DC75FF", 16))
		self.embed.add_field(name="Reglas:", value="1. Ser respetuoso. / 2. No usar lenguaje inapropiado. / 3. No hacer spam. / 4. No server raiding. ", inline=False)
		self.embed.add_field(name="Escribe el siguiente comando si estas de acuerdo:", value="!acepto", inline=False)
		return self.embed
	

def main():

	def create_config_archive():
		template = {
		'prefix': '!', 
		'token': "MTA3NTkwNjEwNTQxNjM1MTgxNQ.Gi9VPl.GgKLRE4hlVLXjltGA1cb4AxT1I-IAu-gLF2Kuo", 
		}
		with open('config.json', 'w') as f:
			json.dump(template, f)


	def read_config_archive():
		with open('config.json') as f:
			config_data = json.load(f)
		return config_data


	if not os.path.exists('config.json'):
		print('Creando archivo de configuración')
		create_config_archive()


	# Parametros iniciales
	config_data = read_config_archive()
	prefix = config_data["prefix"]
	token = config_data["token"]
	intents = discord.Intents.all()
	bot = commands.Bot(
		command_prefix = prefix, 
		intents = intents, 
		description = "Bot moderador")


	# Comandos

	@bot.command(name='acepto', help='Te agrega el rol "usuario"')
	async def add_user_role(ctx):
		# Condicional para que este comando solo se ejecute en MD
		if isinstance(ctx.channel, discord.channel.DMChannel):
			# Obtenemos nuestro servidor mediante la ID
			server = bot.get_guild(1066227032687640607)
			# Obtenemos el rol de usuario de nuestro servidor
			rol = server.get_role(1076328320393805977)
			# Obtenemos al usuario de nuestro servidor mediante su id (la cual viene en el contexto) 
			member = server.get_member(ctx.message.author.id)
			# Le asignamos el rol
			await member.add_roles(rol)
			# Le enviamos un mensaje de bienvenida al servidor
			await ctx.author.send('Te has unido al servidor correctamente, disfruta.')


	# Eventos
	@bot.event
	async def on_member_join(member):
		# ID del canal de bienvenida
		welcome_channel = bot.get_channel(1066227033316806718)
		# Usamos la plantilla para crear la respuesta
		welcome_embed = Welcome_Embed(member.name)
		# Enviamos el embed
		await member.send(embed = welcome_embed.enviar)
		# Damos la bienvenida
		await welcome_channel.send(f'Bienvenido al servidor, {str(member.mention)}. Revisa tus mensajes privados para aceptar las reglas del servidor y poder acceder a los demás canales.')


	@bot.event
	async def on_ready():
		activity = discord.Game(name="A moderar el servidor.")
		await bot.change_presence(activity=activity)
		print('El bot esta funcionando correctamente.')


	bot.run(token)


if __name__ == '__main__':
	main()