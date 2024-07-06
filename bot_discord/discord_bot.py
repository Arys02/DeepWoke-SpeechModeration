import discord
import os
import requests
import websocket
import json

# bot_url = "http://90.60.20.92:8000/classify/"
# bot_url = "ws://localhost:3001"
bot_url = "ws://localhost:3001"


def send_to_model_api(message):
    message_data = {
        "type": "inbound",
        "text": message.content,
        "user": str(message.author),
        "is_hateful": None
    }

    ws.send(json.dumps(message_data))



from dotenv import load_dotenv, dotenv_values

# loading variables from .env file
load_dotenv()

# accessing and printing value
token = os.getenv("DISCORD_API")

ws = websocket.WebSocket()
ws.connect(bot_url)

intents = discord.Intents.all()
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    print(message.author)
    print(message.content)
    send_to_model_api(message)

client.run(token)
# %%
