from helper import module, Message, db
from pyrogram import filters

coreTitle = "flxpr-core"
moduleTitle = "russia 🇷🇺"

commands = ["russia-fix", "russia", "rus"]
arguments = ["on/off/modetwo"]
description = "как russia от амока, только фикшенный"

channel = "@flxpr_modules"
creator = "@flxpr"
website = "flxpr.ru/modules"

@module(cmds=commands, args=arguments, description=description)

async def russia(_, message: Message):
    try:
        text = message.command[1]
        
        await message.edit(
            f"<b>{moduleTitle}</b>"
            f"\n\nrussia let's <b>{text}</b>.."
        )
        db.set(f"rus", text)
        db.set(f"ukr", "off")
        db.set(f"Z", "off")
    except IndexError:
        await message.edit(
            f"<b>{coreTitle}</b>"
            f"\n\nНе указан один из <b>обязательных</b> параметров"
        )


@module(filters.text & filters.me)

async def filter(_, message: Message):
    value = db.get("rus")
    if value == "on":
        text = message.text.replace("з", "<b>Z</b>").replace("в", "<b>V</b>").replace("З", "<b>Z</b>").replace("В", "<b>V</b>").replace("Z", "<b>Z</b>").replace("z", "<b>Z</b>").replace("V", "<b>V</b>").replace("v", "<b>V</b>")
        await message.delete(text)
        await message.reply_text(text, quote=False)
    elif value == "modetwo":
        text = message.text.replace("з", "<b>Z</b>").replace("в", "<b>V</b>").replace("З", "<b>Z</b>").replace("В", "<b>V</b>").replace("Z", "<b>Z</b>").replace("z", "<b>Z</b>").replace("V", "<b>V</b>").replace("v", "<b>V</b>")
        await message.edit(
            f"{text}"
            f" 🇷🇺"
        )
        
made_by = f"{channel} | {creator} | {website}"
