import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from commands import *
from pwdmanager import pwdgen as pg
from pwdmanager import (insert, read_all, search, create_table)
import datetime
import pytz

# Client setup
pwdmanager = Client(
    "PasswordGenerator",
    bot_token=os.environ["BOT_TOKEN"],
    api_id=int(os.environ["API_ID"]),
    api_hash=os.environ["API_HASH"]
)

create_table()

# Start Command
@pwdmanager.on_message(filters.private & filters.command(start_command))
async def start(bot, message, cq=False):
    buttons = [
        [InlineKeyboardButton('👉 Help here ', callback_data='help')],
        [InlineKeyboardButton('Random Password', switch_inline_query_current_chat='/randpwd '),
         InlineKeyboardButton('Specific Password', switch_inline_query_current_chat='/specpwd ')]
    ]

    if cq:
        await message.message.edit(
            text=start_msg.format(message.from_user.mention),
            reply_markup=InlineKeyboardMarkup(buttons),
        )

    else:
        await message.reply_text(
            text=start_msg.format(message.from_user.mention),
            reply_markup=InlineKeyboardMarkup(buttons),
            quote=True
        )


# Help Command
@pwdmanager.on_message(filters.command(help_command))
async def help(bot, update):
    buttons = [
        [InlineKeyboardButton('Random Password', switch_inline_query_current_chat='/randpwd '),
         InlineKeyboardButton('Specific Password', switch_inline_query_current_chat='/specpwd ')],
        [InlineKeyboardButton('💾 All Passwords', switch_inline_query_current_chat='/mypwds'),
         InlineKeyboardButton('🔎 Search Password', switch_inline_query_current_chat='/search ')]
    ]
    await update.reply_text(
        text=help_msg,
        quote=True,
        reply_markup=InlineKeyboardMarkup(buttons)
    )


# help callback
@pwdmanager.on_callback_query(filters.create(lambda _, __, query: query.data.startswith('help')))
async def help_cq(bot, message):
    await message.answer()
    buttons = [
        [InlineKeyboardButton('Random Password', switch_inline_query_current_chat='/randpwd '),
         InlineKeyboardButton('Specific Password', switch_inline_query_current_chat='/specpwd ')],
        [InlineKeyboardButton('💾 All Passwords', switch_inline_query_current_chat='/mypwds'),
         InlineKeyboardButton('🔎 Search Password', switch_inline_query_current_chat='/search ')],
        [InlineKeyboardButton("Back", callback_data='start'), InlineKeyboardButton("Close", callback_data='close')]
    ]
    await message.message.edit(
        text=help_msg,
        reply_markup=InlineKeyboardMarkup(buttons)
    )


# close callback
@pwdmanager.on_callback_query(filters.create(lambda _, __, query: query.data.startswith("close")))
async def close_cq(bot, message):
    await message.message.delete()
    await message.message.reply_to_message.delete()


# start callback
@pwdmanager.on_callback_query(filters.create(lambda _, __, query: query.data.startswith("start")))
async def start_cq(bot, message):
    await message.answer()
    await start(bot, message, True)


# message handling
@pwdmanager.on_message((filters.text | filters.forwarded | filters.reply) & filters.private)
async def reply(bot, message):
    chat_id = int(message.chat.id)
    text = str(message.text)
    msg_list = text.split(' ')
    username = message.chat.username

    if msg_list[0] in [os.environ.get('BOT_USERNAME')]:
        msg_list.pop(0)
    else:
        pass

    # randpwd command
    if msg_list[0] == '/' + gen_random_pwd_command[0]:
        if len(msg_list) >= 3:
            try:
                length = int(msg_list[1])
            except:
                length = 12
            info = ' '.join([str(item) for item in msg_list[2:]])
        else:
            try:
                length = int(msg_list[1])
            except:
                length = 12
            info = 'No info given'
        password = pg(length=length)
        dt = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
        dtf = dt.strftime("%d/%m/%Y %H:%M:%S")
        reply_text = pwd_msg.format(
            password,
            info
        )

        insert(chat_id, password, info, username, dtf)

        await message.reply_text(text=reply_text, quote=True)

    # specpwd command
    if msg_list[0] == '/' + gen_spec_pwd_command[0]:
        if len(msg_list) == 1:
            reply_text = f"Your command should look like this - /specpwd **<**<code>char</code>**> <**<code>len</code>**> <**<code>info</code>**>**\n/help for more info."

        else:
            char = msg_list[1]
            char_set = list(char)
            if len(msg_list) >= 4:
                try:
                    length = int(msg_list[2])
                except:
                    length = 12
                info = ' '.join([str(item) for item in msg_list[3:]])
            else:
                try:
                    length = int(msg_list[2])
                except:
                    length = 12
                info = 'No info given'
            password = pg(length=length, set=char_set)
            dt = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
            dtf = dt.strftime("%d/%m/%Y %H:%M:%S")
            reply_text = pwd_msg.format(
                password,
                info
            )

            insert(chat_id, password, info, username, dtf)

        await message.reply_text(text=reply_text, quote=True)

    # mypwds command
    if msg_list[0] == '/' + my_pwds_command[0]:
        rows = read_all(chat_id)
        if len(rows) > 0:
            reply_text = "**Here are your all passwords:**\n\n"
            for row in rows:
                pwd, info, dt = row[1], row[2], row[4]
                reply_text = reply_text + f"**Password:** <code>{pwd}</code>\n**Info:** --{info}--\n**Saved at** __{dt}__\n\n"
        else:
            reply_text = "You don't have any saved passwords yet."

        await message.reply_text(text=reply_text, quote=True)
        # with io.BytesIO(str.encode(reply_text)) as file:
        #     file.name = 'passwords.txt'
        #     await bot.send_document(chat_id=chat_id, document=file)

    # search command
    if msg_list[0].lower() == '/' + search_pwd_command[0]:
        if len(msg_list) == 1:
            reply_text = "Please provide info to search for in passwords. For more- /help"
        else:
            to_srch = msg_list[1]
            rows = search(chat_id, to_srch)
            if len(rows) > 0:
                srch_reply_text = ''
                for row in rows:
                    pwd, info, dt = row[1], row[2], row[4]
                    srch_reply_text = srch_reply_text + f"**Password:** <code>{pwd}</code>\n**Info:** --{info}--\n**Saved at** __{dt}__\n\n"
                reply_text = f"**Here are your passwords in search of --{to_srch}--:**\n\n" + srch_reply_text
            else:
                reply_text = f"No password found in search of {to_srch}!"

        await message.reply_text(text=reply_text, quote=True)


# running bot..
pwdmanager.run()
