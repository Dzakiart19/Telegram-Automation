import asyncio
import pickle
from telethon import TelegramClient

API_ID = '26372402'
API_HASH = 'a2732d77a9abc513db065170f563a603'
PHONE = '+6285962694573'
SESSION_NAME = 'tele_prod_new'


async def main():
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    await client.connect()
    if await client.is_user_authorized():
        me = await client.get_me()
        print(f"ALREADY_AUTHORIZED: {me.first_name} (@{me.username})")
        await client.disconnect()
        return
    result = await client.send_code_request(PHONE)
    with open('.login_state.pkl', 'wb') as f:
        pickle.dump({'phone_code_hash': result.phone_code_hash}, f)
    print("CODE_SENT")
    await client.disconnect()


asyncio.run(main())
