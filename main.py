import os
import asyncio
import random
from keep_alive import keep_alive
from telethon import TelegramClient, events

list_bhati = ['bhati op', 'machaya bhati']
greetings = ['hi', 'hey', 'hello', 'hi!', 'hey!', 'hello!', 'heya', 'sup']

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
phone = os.getenv('PHONE')

client = TelegramClient('tele', api_id, api_hash)
client.start(phone=phone)



def make_handler(dicta):
    async def handler(event):
        if event.out:
            return
        message = event.message.message.lower().strip()
        await asyncio.sleep(5)
        for x in list_bhati:
            if message == x:
                await event.reply('Bhati always OP!')
                return
        for y in greetings:
            if message == y:
                await event.respond(random.choice(greetings).capitalize())
                return
        for item, reply in dicta.items():
            if message == item:
                await event.respond(reply)
                return
    return handler


contacts = {
    'Bansal':   {'aur bta bro': 'wahi same bhai. tu bta', 'oye': 'bol'},
    'Saumil':   {'sun': 'bol', 'oye': 'bol', 'aur bta': 'wahi same bhai. tu bta'},
    'Bhati':    {'sun': 'bol', 'oye': 'bol', 'kya kar raha hai': 'kuch nahi. bata'},
    'Me':       {'aur bta': 'wahi same bhai. tu bta', 'oye': 'bol'},
    'Adit':     {'aur bta': 'wahi same bhai. tu bta', 'oye': 'bol'},
    'Tanishka': {'aur bta': 'wahi same bro. tu bta', 'oye': 'bol'},
    'Akshay':   {'aur bta': 'wahi same bhai. tu bta', 'oye': 'bol'},
    'Anshu':    {'aur bta': 'wahi same bro. tu bta', 'oye': 'bol'},
    'Nandana':  {'aur bta': 'wahi same bro. tu bta', 'oye': 'bol'},
    'Shruti':   {'aur bta': 'wahi same bro. tu bta', 'oye': 'bol'},
}

for env_key, dicta in contacts.items():
    chat = os.getenv(env_key)
    if chat:
        client.add_event_handler(
            make_handler(dicta),
            events.NewMessage(chats=chat, incoming=True)
        )

keep_alive()
client.run_until_disconnected()
