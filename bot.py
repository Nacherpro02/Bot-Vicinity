import os
import discord
from discord.ext import commands
from discord import app_commands
import asyncio
from dotenv import load_dotenv
import aiohttp
import random

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
exe = True

integrantes = ["Javi", "Juanjo", "Nacher", "Ruski", "Picapiedra"]

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True
intents.voice_states = True
channel_id = 1311745347848110091 
url = "https://www.vicinityclo.de/products/akimbo-lows-pristina-moss"
#url = "https://github.com/Nacherpro02"
GUILD_ID = discord.Object(id=os.getenv('GUILD_ID'))
isplaying = True

client = commands.Bot(command_prefix='!', intents=intents)

ruta_audio = 'alarma.mp3'
@client.command()
async def ping(ctx):
    await ctx.send(f'Pons 🐎! {round(client.latency * 1000)}ms')


def get_random_time():
    """Genera un número aleatorio entre 30 y 60 segundos."""
    return random.randint(30,60)



async def check_http_and_notify():
    print("Verificando la URL...")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                status = response.status
                print(f"Estado HTTP: {status}")  
        return status
    except Exception as e:
        print(f"Error al verificar la URL: {e}")


@client.command()
async def req(ctx):
    global exe
    await ctx.send("Comando ejecutando...")
    print("Iniciando el bucle principal...")  
    while exe == True:
        try:
            status = await check_http_and_notify()
            if status == 200:
                print("Código 200 encontrado, enviando mensaje a Discord.")
                await ctx.send("¡La URL ha respondido con un código 200!")
                await ctx.send(f"Aqui lo podeis comprar hijos de puta: {url}")
                await ctx.send("Vamos a reproducir el audio de la alarma...")
                await ctx.send("@everyone Despertad Hijos de Puta")
                canal = ctx.guild.voice_channels[0]
                while isplaying == True:  
                    voz = await canal.connect()
                    voz.play(discord.FFmpegPCMAudio(ruta_audio), after=lambda e: print('Audio terminado'))
                
                    while voz.is_playing():
                        await asyncio.sleep(1)
                
              
                    await voz.disconnect()
            else:
                print(f"Respuesta HTTP: {status}. No se envió mensaje.")
                await ctx.send(f"¡La URL no está disponible, código {status}!")      
        except Exception as e:
            print(f"Error al verificar la URL: {e}")
        
  
        await asyncio.sleep(get_random_time())



@client.command()
async def hola(ctx):
    name = ctx.author.display_name
    await ctx.send(f"¡Hola {name}!, Estas chill de cojones: 😎")
    await ctx.send(f"Pareces a este pibe:")
    url_img = "https://images.ecestaticos.com/FT4j1yrH6ubzFmRZSFIt-7IiXy4=/0x0:768x432/1200x900/filters:fill(white):format(jpg)/f.elconfidencial.com%2Foriginal%2Fcc1%2F688%2F7d3%2Fcc16887d325ecbce718eaa217416f1bf.jpg"
    await asyncio.sleep(1)
    await ctx.send(url_img)


@client.command()
async def akimbo(ctx):
    await ctx.send(f"URL: {url}")
    
@client.command()
async def javi(ctx):
    await ctx.send("Javi guapo 😘")

@client.command()
async def canijo(ctx):
    for name in integrantes:
        await ctx.send(f"Integrante: {name}")

@client.command()
async def comandos(ctx):
    await ctx.send("Comandos disponibles: !ping, !req, !akimbo, !javi, !canijo, !stop, !comandos, !hola, !repositorio, !delete_chat")

@client.command()
async def repositorio(ctx):
    await ctx.send("https://github.com/Nacherpro02/Bot-Vicinity")

@client.command()
@commands.has_permissions(manage_messages=True) 
async def delete_chat(ctx):
    await ctx.send("Borrando todos los mensajes... Esto puede tardar un momento.")
  
    deleted = 0
    while True:
   
        try:
            deleted_messages = await ctx.channel.purge(limit=100)
            deleted += len(deleted_messages)
            if len(deleted_messages) < 100:
                break
        except discord.Forbidden:
            await ctx.send("No tengo permiso para gestionar mensajes en este canal.")
            return
        except discord.HTTPException:
            await ctx.send("Ocurrió un error al intentar borrar los mensajes.")
            return

    await ctx.send(f'Se han borrado un total de {deleted} mensajes.', delete_after=5) 


@client.command()
async def stop(ctx):
    global exe
    exe = False
    await ctx.send("Bucle principal detenido.")

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('/help para comandos'))
    print(f'{client.user} has connected to Discord!')

    print(f'{client.user} se ha conectado a Discord!')



@client.event
async def on_message(message):
    if message.author == client.user:
        return
    await client.process_commands(message)

client.run(TOKEN)
