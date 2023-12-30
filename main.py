import discord
import os
from discord.ext import commands
from discord import app_commands
from keep_alive import keep_alive
import requests
import asyncio
import datetime
import pytz
import random
import urllib.parse
import json
import schedule
import cloudinary
from cloudinary import uploader
from PIL import Image
from io import BytesIO

cloudinary.config( 
  cloud_name = "dblmwxdcc", 
  api_key = "537679287457256", 
  api_secret = "KvYeXLrGNf8iYanW2kKojXUDqa8" 
)


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!cat ", intents=intents)

my_secret = os.environ['discordToken']
thecatAPI = os.environ['catAPIkey']

channelDev = 1186227913167753286

channelServers = {}
configFileName = 'dailychannelservers.json'


@bot.tree.command(name="ping", description="Ping the bot")
async def slash_command(interaction: discord.Interaction):
  await interaction.response.send_message("Pong!")

@bot.command('texto')
async def test(ctx,  *, args: str):

  try:
    url = "https://api.thecatapi.com/v1/images/search"
    headers = {'x-api-key': thecatAPI}
    params = {
        'limit': 1,
    }
  
    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    imageURL = data[0]['url']
    imageResponse = requests.get(imageURL)
    imageData = imageResponse.content

    imageWidth = data[0]['width']
    imageHeight = data[0]['height']
    textSize = 15
    
    if imageWidth >= 100 and imageWidth <= 500:
      textSize = 25
    elif imageWidth >= 500 and imageWidth <= 1000:
      textSize = 50
    elif imageWidth >= 1000 and imageWidth <= 1400:
      textSize = 100
    elif imageWidth >= 1400 and imageWidth<= 1800:
      textSize = 150
    elif imageWidth >= 1800 and imageWidth<= 2400:
      textSize = 200
    elif imageWidth >= 2400 and imageWidth<= 2800:
      textSize = 250

    
    with open('imagescats/catText.jpg', 'wb') as file:
      file.write(imageData)
    
    
    imagePath = 'imagescats/catText.jpg'
    upload_result = uploader.upload(
        imagePath,
        public_id="catText",
        transformation=[
          {'color': "#FFFFFF", 'width': imageWidth, 'height': imageHeight, 'overlay': {'font_family': "arial", 'font_size': textSize, 'font_weight': "bold", 'text_align': "left", 'text': f'{args}'}, 'crop': "fit"},
          {'flags': "layer_apply", 'gravity': "south", 'y': 45}
          ])
    
    await ctx.send(upload_result["secure_url"])
    
  except Exception as e:
    await ctx.send(
        f"Parece que houve algum problema de conexão. Tente mais tarde! 😿"
    )


@bot.command('ajuda')
async def ajuda(ctx):
  await ctx.send(
      f'Olá! Me chamo Cat Bot e minha função é melhorar seu dia 😺\n\n'
      f'*✅ Funcional    ☑️ Funcional, porém pode ocorrer alguns problemas    ♨️ Em desenvolvimento    ❌ Não está disponível no momento* \n\n'
      f'**Comandos:**\n\n'
      f'✅  !cat sobre\n'
      f'✅  !cat imagem (imagem aleatória de um gatinho 🐱)\n'
      f'❌  !cat gifcat (gif aleatório de um gatinho 🐱)\n'
      f'✅  !cat texto ~*digite um texto*~ (cria uma imagem com seu texto e um gatinho aleatório)\n'
      f'✅  !cat daily (imagem diária de um gatinho 😼)\n'
      f'✅  !cat dailychat  (mande no canal onde eu deva enviar as atuailizações do DAILY CAT 😺) **1 CANAL POR SERVIDOR**\n'
  )


@bot.command('sobre')
async def sobre(ctx):
  userID = 519659484583428109
  targetUser = await bot.fetch_user(userID)
  await ctx.send(
      f'Olá! Me chamo Cat Bot e ainda estou em desenvolvimento. Atualmente sou codado pelo arrombado do {targetUser.mention} 😼. Ele ainda tem muitas ideias para mim, mas vai levar um tempo para ele criar vergonha na cara e implementar elas. Até lá, espero conseguir melhorar seu dia com as funcionalidades que tenho por enquanto, tente chamar !cat ajuda 😺.'
  )


@bot.command('imagem')
async def imagem(ctx):

  try:
    url = "https://api.thecatapi.com/v1/images/search"
    headers = {'x-api-key': thecatAPI}
    params = {
        'limit': 1,
    }

    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    await ctx.send(data[0]['url'])

  except Exception as e:
    await ctx.send(f"Erro de conexão com a API 😿. Tente mais tarde!")


@bot.command('gifcat')
async def gif(ctx):
  try:
    urlAPI = f"https://cataas.com/cat/gif"
    response = requests.get(urlAPI)
    data = response.content
    with open("gatoGIF.gif", "wb") as f:
      f.write(data)
    with open("gatoGIF.gif", "rb") as f:
      await ctx.send(file=discord.File(f))
  except Exception as e:
    await ctx.send(
        f"Parece que o cataas API está com problemas de conexão. Tente mais tarde! 😿"
    )


@bot.command('')
async def textoImagem(ctx, *, args: str):
  try:
    argsList = args.split()

    color = '#ffff'
    font = 'Arial'
    color = urllib.parse.quote(color)
    size = '65'

    urlAPI = f"https://cataas.com/cat?json=true"
    response = requests.get(urlAPI)
    data = response.json()
    catId = data['_id']
    textURL = urllib.parse.quote(args)

    if len(args) >= 30:
      await ctx.send(
          "Opa opa opa! Isso não é podcast não amigo, envie um texto menor 😾")
      return

    url = f"https://cataas.com/cat/{catId}/says/{textURL}?font={font}&fontSize={size}&fontColor={color}&fontBackground=none&position=bottom"
    await ctx.send(url)

  except Exception as e:
    await ctx.send(
        f"Parece que o cataas API está com problemas de conexão. Tente mais tarde! 😿"
    )


@bot.command('daily')
async def catDaily(ctx):
  brazilTimezone = pytz.timezone('America/Sao_Paulo')
  now = datetime.datetime.now(brazilTimezone)
  if now.month == 12 and now.day == 25:
    with open("imagescats/specialdates/12_25/gato-natal.gif", "rb") as f:
      await ctx.send("Esse é o **DAILY CAT** DE HOJE, **FELIZ NATAL**!", file=discord.File(f))
      await ctx.send("Todos os dias à MEIA NOITE o **DAILY CAT** é atualizado! 😼")
  else:
    with open("imagescats/cat.jpg", "rb") as f:
      await ctx.send("Esse é o **DAILY CAT** de hoje!", file=discord.File(f))
      await ctx.send("Todos os dias à MEIA NOITE o **DAILY CAT** é atualizado! 😼")


@bot.command('dailychat')
async def dailyConfig(ctx):
  serverID = str(ctx.guild.id)
  channelID = ctx.channel.id
  global channelDev
  guild = bot.get_guild(int(serverID))
  channel = bot.get_channel(channelID)

  global channelServers
  if serverID not in channelServers:
    channelServers[serverID] = {"channelID": channelID}
    await saveConfigFile(channelServers)
    await ctx.send(
        f'Canal salvo! As próximas atualizações do DAILY CAT serão enviadas aqui 😸'
    )
    await bot.get_channel(channelDev).send(
        f'Servidor: {guild.name}, Canal: {channel.name} || ADICIONOU O DAILY CAT!'
    )
  elif channelServers[serverID]["channelID"] != channelID:
    channelServers[serverID]["channelID"] = channelID
    await saveConfigFile(channelServers)
    await ctx.send(
        f'Canal atualizado! As próximas atualizações do DAILY CAT serão enviadas aqui 😸'
    )
    await bot.get_channel(channelDev).send(
        f'Servidor: {guild.name}, Canal: {channel.name} || ATUALIZOU O CANAL DO DAILY CAT!'
    )
  else:
    await ctx.send(
        'Este canal já está configurado para receber as atualizações do DAILY CAT.'
    )


async def schedule_catDaily():


  while True:
    brazilTimezone = pytz.timezone('America/Sao_Paulo')
    now = datetime.datetime.now(brazilTimezone)
    then = now + datetime.timedelta(days=1)
    then = then.replace(hour=0, minute=0, second=1)
    waitTime = (then - now).total_seconds()

    await asyncio.sleep(waitTime)
    global channelServers
    
    #global channelDev
    #channelDev2 = bot.get_channel(channelDev)

    try:
      
      url = "https://cataas.com/cat"
      response = requests.get(url)
      image = response.content
      with open("imagescats/catDaily.jpg", "wb") as f:
        f.write(image)   
      
      #url = "https://api.thecatapi.com/v1/images/search?limit=1"
      #headers = {'x-api-key': thecatAPI}
      #response = requests.get(url, headers=headers)
      #data = response.json()
      #imageURL = data[0]['url']
      #imageResponse = requests.get(imageURL)
      #imageData = BytesIO(imageResponse.content)
      #img = Image.open(imageData)
      #img.save('imagescats/catDaily.jpg')
      
      for serverID, serverData in channelServers.items():
        channelID = serverData["channelID"]
        channel = bot.get_channel(channelID)
        brazilTimezone = pytz.timezone('America/Sao_Paulo')
        now = datetime.datetime.now(brazilTimezone)
        if now.month == 12 and now.day == 25:
          if channel is not None:
            with open("imagescats/specialdates/12_25/gato-natal.gif", "rb") as f:
              await channel.send(f'DAILY CAT NATALINO! 🐱 ', file=discord.File(f))
            with open("imagescats/specialdates/12_25/catvideo.mp4", "rb") as f:
              await channel.send(f'FELIZ NATAL! 🐱 ', file=discord.File(f))
        else:
          if channel is not None:
            with open("imagescats/catDaily.jpg", "rb") as f:
              await channel.send("DAILY CAT! 🐱", file=discord.File(f))
    except Exception as e:
      for serverID, serverData in channelServers.items():
        channelID = serverData["channelID"]
        channel = bot.get_channel(channelID)
        await channel.send(
            f"Parece que houve problemas de conexão com a API. Infelizmente o DAILY CAT não ocorrerá hoje 😿"
        )


async def saveConfigFile(config):
  with open(configFileName, "w") as f:
    json.dump(config, f, indent=4)


async def loadConfigFile():
  with open(configFileName, 'r') as f:
    return json.load(f)


@bot.event
async def on_ready():
  global channelServers
  global channelDev

  brazilTimezone = pytz.timezone('America/Sao_Paulo')
  now = datetime.datetime.now(brazilTimezone)

  await bot.get_channel(channelDev).send(
      f'Estou inicializando... || {now.day}/{now.month}/{now.year} às {now.hour}:{now.minute}:{now.second}'
  )

  channelServers = await loadConfigFile()
  await bot.tree.sync()
  await schedule_catDaily()


if __name__ == '__main__':
  keep_alive()
  bot.run(my_secret)
