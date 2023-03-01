import json, os
import datetime
import discord
import asyncio
import random
from discord.ext.commands import has_any_role
from discord.ext import commands
from dotenv import load_dotenv
from db import database
from dataclasses import dataclass
from discord import Member, Guild


@dataclass
class Welcome_Embed():
    member: str

    def enviar(self):
        self.embed = discord.Embed(title=f"Hola {self.member}. Para unirte al servidor debes aceptar las siguientes reglas...", colour=int("DC75FF", 16))
        self.embed.add_field(name="Reglas:", value="1. Ser respetuoso. / 2. No usar lenguaje inapropiado. / 3. No hacer spam. / 4. No server raiding. ", inline=False)
        self.embed.add_field(name="Escribe el siguiente comando si estas de acuerdo:", value="acepto", inline=False)
        return self.embed
    
    
def main():

    bot = commands.Bot(command_prefix='', description="This is a helper bot")

    def create_config_archive():
        template = {
        'prefix': '', 
        'token': "TOKEN AQUI", 
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
    load_dotenv()
    config_data = read_config_archive()
    prefix = config_data["prefix"]
    token = config_data["token"]
    intents = discord.Intents.all()
    bot = commands.Bot(
        command_prefix = prefix, 
        intents = intents, 
        description = "Bot moderador")


    # Comandos

    async def enviar_recordatorio():
        await bot.wait_until_ready()
        while not bot.is_closed():
            fecha_entrega = datetime.datetime.now() + datetime.timedelta(days=7) # Cambia esto para establecer la fecha límite deseada
            canal_general = bot.get_channel(ID) # Reemplaza "ID_DEL_CANAL_GENERAL" con el ID del canal general de tu servidor de Discord.
            mensaje_recordatorio = f'¡Recuerden que la fecha límite de entrega es {fecha_entrega.strftime("%d/%m/%Y")}!'
            await canal_general.send(mensaje_recordatorio)
            await asyncio.sleep(60*60*24) # Establece la frecuencia deseada del recordatorio en segundos (en este caso, un día completo)

    bot.loop.create_task(enviar_recordatorio())
    #Crea una fecha final para el juego AI

    #los registra en la DB pero falta crear "insert_one" para que pueda guardar documentos la base de datos
    @bot.command(help="registrate en la database")
    async def register(ctx):
        flag =database.verify_id(connection, str(ctx.author.id))
        if flag:
            await ctx.send("Usted ya se encuentra registrado en la base de datos")
        else:
            database.register(connection, ctx)
            await ctx.send("Te has registrado correctamente en la base de datos")


    @bot.command(help='Muestra las palabras clavse para hablar con el bot')
    async def comandos(ctx):
        embed = discord.Embed(title=f"{ctx.guild.name}",description="aqui va una lista de los comandos para que el bot responda   1.Saluda   /  2.Quien es mi amigo invisible  /  3.Mostrame la lista de deseados de @naza  ... ",
        timestamp=datetime.datetime.utcnow(), color = discord.Color.blue())
        embed.set_thumbnail(url="https://www.clipartmax.com/png/middle/72-720707_imagenes-sin-fondo-renders-png-renders-sin-fondo.png")

        await ctx.send(embed=embed)

    @bot.command(name='Saluda')
    async def greet(ctx):
        await ctx.send('¡Hola!')

    @bot.command(name='acepto', help='Te agrega el rol "usuario"')
    async def add_user_role(ctx):
        # Condicional para que este comando solo se ejecute en MD
        if isinstance(ctx.channel, discord.channel.DMChannel):
            # Obtenemos nuestro servidor mediante la ID
            server = bot.get_guild("IDserver")
            # Obtenemos el rol de usuario de nuestro servidor
            rol = server.get_role("IDrol")
            # Obtenemos al usuario de nuestro servidor mediante su id (la cual viene en el contexto) 
            member = server.get_member(ctx.message.author.id)
            # Le asignamos el rol
            await member.add_roles(rol)
            # Le enviamos un mensaje de bienvenida al servidor
            await ctx.author.send('Te has unido al servidor correctamente, disfruta.')


    # Eventos
    @bot.event
    async def on_member_join(member: Member):
        # get server member
        guild_member: Guild = member.guild
        # get text chennels id
        text_channels = guild_member.text_channels
        # ID del canal de bienvenida
        welcome_channel = text_channels[0]
        # Usamos la plantilla para crear la respuesta
        welcome_embed = Welcome_Embed(member=member.name)
        # Enviamos el embed
        await member.send(embed = welcome_embed.enviar())
        # Damos la bienvenida
        await welcome_channel.send(f'Bienvenido al servidor, escribiendo "help o comandos" (PODRAS VER LAS PALABRAS CLAVES PARA INTERACTUAR CONMIGO) {str(member.mention)}. Revisa tus mensajes privados para aceptar las reglas del servidor y poder acceder a los demás canales.')

    @bot.event
    async def on_ready():
        global connection
        connection = database.db_connect()
        print("[BOT]: Ready")


    bot.run(token)


if __name__ == '__main__':
    main()