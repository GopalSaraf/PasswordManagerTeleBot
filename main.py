import os 
from os import error
import logging
import pyrogram
from decouple import config
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.types import User, Message
from commands import *
from pwdgen import pwdgen as pg
from pwdgen import savepwd as sp

firstclient = Client(
    "PasswordGenerator",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"]
)

# Start Command
@firstclient.on_message(filters.command(start_command))
async def start(bot, update):
    await update.reply_text(
    text=start_msg.format(update.from_user.mention)
    )

# Help Command
@firstclient.on_message(filters.command(help_command))
async def help(bot, update):
    await update.reply_text(
    text=help_msg,
    )


@firstclient.on_message((filters.text | filters.forwarded | filters.reply) & filters.private)
async def reply(bot, message):
  chat_id = int(message.chat.id)
  text = str(message.text)
  msg_list = text.split(' ')

# randpwd command
  if msg_list[0] == '/' + gen_random_pwd_command[0]:
    if len(msg_list) >= 3:
        try:
            length = int(msg_list[1])
        except:
            length = 8
        info = ' '.join([str(item) for item in msg_list[2:]])
    else:
        try:
            length = int(msg_list[1])
        except:
            length = 8
        info = 'No info given.'
    password = pg(length=length)
    reply_text = pwd_msg.format(
    password,
    info    
    )
    sp(password,info)
    
# specpwd command
  if msg_list[0] == '/' + gen_spec_pwd_command[0]:
    if len(msg_list) == 1:
        reply_text = f"Characters are compulsory for /{gen_spec_pwd_command[0]}. For more info- /help"
    else:
        char = msg_list[1]
        char_set = list(char)
        if len(msg_list) >= 4:
            try:
                length = int(msg_list[2])
            except:
                length = 8
            info = ' '.join([str(item) for item in msg_list[3:]])
        else:
            try:
                length = int(msg_list[2])
            except:
                length = 8
            info = 'No info given.'
        password = pg(length=length,set=char_set)
        reply_text = pwd_msg.format(
        password,
        info    
        )
        sp(password,info)
            
    await bot.send_message(text=reply_text, chat_id=chat_id)

# mypwds command
@firstclient.on_message(filters.command(my_pwds_command))
async def mypwds(bot, update):
    chat_id = int(message.chat.id)
    with open("SavedPasswords.txt") as file:
        await bot.send_document(chat_id, file, caption="Your Passwords!")
    
    
    
firstclient.run()
