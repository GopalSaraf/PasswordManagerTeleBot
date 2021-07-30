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
import datetime
import pytz


firstclient = Client(
    "PasswordGenerator",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"]
)

saved_passwords = {}

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
            info = 'No info given'
        password = pg(length=length)
        dt = datetime.datetime.now(pytz.timezone('Asia/Kolkata')) 
        dtf = dt.strftime("%d/%m/%Y %H:%M:%S")
        reply_text = pwd_msg.format(
            password,
            info
        )
        
        if chat_id in saved_passwords:
            saved_passwords[chat_id] += [[info, password, dtf]]
        else:
            saved_passwords[chat_id] = [[info, password, dtf]]
        
        await bot.send_message(text=reply_text, chat_id=chat_id)
        

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
                info = 'No info given'
            password = pg(length=length, set=char_set)
            dt = datetime.datetime.now(pytz.timezone('Asia/Kolkata')) 
            dtf = dt.strftime("%d/%m/%Y %H:%M:%S")
            reply_text = pwd_msg.format(
                password,
                info
            )
            
            if chat_id in saved_passwords:
                saved_passwords[chat_id] += [[info, password, dtf]]
            else:
                saved_passwords[chat_id] = [[info, password, dtf]]        
         
        await bot.send_message(text=reply_text, chat_id=chat_id)
 
    # mypwds command
    if msg_list[0] == '/' + my_pwds_command[0]:
        if chat_id in saved_passwords:            
            reply_text = "**Here are your all passwords:**\n\n"
            for pwds in saved_passwords[chat_id]:
                info, pwd, dt = pwds
                reply_text = reply_text + f"**Password:** <code>{pwd}</code>\n**Info:** __{info}__\nSaved at {dt}\n\n"
        else:
            reply_text="You don't have any saved passwords yet."
            
        await bot.send_message(text=reply_text, chat_id=chat_id)
        
    # search command
    if msg_list[0] == '/' + search_pwd_command[0]:
        if chat_id in saved_passwords:
            if len(msg_list) == 1:
                reply_text = "Please provide info to search for in passwords. For more- /help"
            else:
                to_srch = msg_list[1]
                srch_reply_text = ''
                for pwds in saved_passwords[chat_id]:
                    if to_srch.lower() in pwds[0].lower():
                        info, pwd, dt = pwds
                        srch_reply_text = srch_reply_text + f"**Password:** <code>{pwd}</code>\n**Info:** __{info}__\nSaved at {dt}\n\n"
                if srch_reply_text == '':
                    reply_text = f"No password found in search of {to_srch}!"
                else:
                    reply_text = f"**Here are your passwords in search of {to_srch}:**\n\n" + srch_reply_text
                    
        else:
            reply_text="You don't have any saved passwords yet to search in for."
                
        await bot.send_message(text=reply_text, chat_id=chat_id)
    
    
firstclient.run()
