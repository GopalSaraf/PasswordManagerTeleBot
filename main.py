import os 
from os import error
import logging
import pyrogram
from decouple import config
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.types import User, Message
import random

firstclient = Client(
  "SampleBot",
  bot_token = "1811277952:AAHmerb6PEqYNCRqQfnI5B9s_Bt1wzHfdqg",
  api_id = 4072549
  api_hash = "9004f340b4b8fde2a93ab021a130fe9b"
)

start_string = "Hi {},\nI am a sample bot"

@firstclient.on_message(filters.command(["start"]))
async def start(bot, update):
  await update.reply_text(
  text=start_string.format(update.from_user.mention)
  )
  
@firstclient.on_message((filters.text | filters.forwarded | filters.reply) & filters.private)
async def reply(bot, message):
  chat_id = int(message.chat.id)
  text = str(message.text)
  reply_text = f"**Here's is your message:**\n<code>{text}</code>\n\nThank You!"
  await bot.send_message(text=reply_text, chat_id=chat_id)
  
firstclient.run()
