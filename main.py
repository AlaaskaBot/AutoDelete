from time import time
from os import getenv
from subprocess import Popen
from pyrogram import Client, filters
from utils.info import *
from utils.database import *

# Read API credentials from environment
api_id = int(getenv("API_ID"))
api_hash = getenv("API_HASH")
bot_token = getenv("BOT_TOKEN")
port = int(getenv("PORT", 8080))  # default fallback if PORT is not set

User = Client(
    "auto-delete-user",
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token
)

@User.on_message(filters.chat(CHATS))
async def delete(user, message):
    try:
        if bool(WHITE_LIST):
            if message.from_user.id in WHITE_LIST:
                return 
        if bool(BLACK_LIST):
            if message.from_user.id not in BLACK_LIST:
                return
        _time = int(time()) + TIME 
        save_message(message, _time)
    except Exception as e:
        print(str(e))

@User.on_message(filters.regex("!start") & filters.private)
async def start(user, message):
    await message.reply("Hi, I'm alive!")

# Start the server and the delete script
Popen(f"gunicorn utils.server:app --bind 0.0.0.0:{port}", shell=True)
Popen("python3 -m utils.delete", shell=True)
User.run()
