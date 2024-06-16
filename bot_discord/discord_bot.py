import discord
import os
import requests

bot_url = "http://90.60.20.92:8000/classify/"


def send_to_model_api(message) -> float:
    message_obj = {"text": message}
    response = requests.post(bot_url, json=message_obj)
    return float(response.json()['class'])


from dotenv import load_dotenv, dotenv_values

# loading variables from .env file
load_dotenv()

# accessing and printing value
token = os.getenv("DISCORD_API")

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
    response = send_to_model_api(message.content)
    print(response)
    if response > 0.5:
        await message.channel.send("PROBLÉMATIQUE !!!")


client.run(token)