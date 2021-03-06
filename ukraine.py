from helper import module, Message, db
from pyrogram import filters

coreTitle = "flxpr-core"
moduleTitle = "ukraine 🇺🇦"

commands = ["ukraine", "ukr"]
arguments = ["on/off/modetwo"]
description = "как russia - только полная противоположность, заменяет буквы Z, V, з, в на их зачеркнутые версии"

channel = "@flxpr_modules"
creator = "@flxpr"
website = "flxpr.ru/modules"

@module(cmds=commands, args=arguments, description=description)

async def ukraine(_, message: Message):
    try:
        text = message.command[1]
        
        await message.edit(
            f"<b>{moduleTitle}</b>"
            f"\n\nukraine let's <b>{text}</b>.."
        )
        db.set(f"ukr", text)
        db.set(f"rus", "off")
        db.set(f"Z", "off")
    except IndexError:
        await message.edit(
            f"<b>{coreTitle}</b>"
            f"\n\nНе указан один из <b>обязательных</b> параметров"
        )


@module(filters.text & filters.me)

async def filter(_, message: Message):
    value = db.get("ukr")
    if value == "on":
        text = message.text.replace("з", "<s>Z</s>").replace("в", "<s>V</s>").replace("З", "<s>Z</s>").replace("В", "<s>V</s>").replace("Z", "<s>Z</s>").replace("z", "<s>Z</s>").replace("V", "<s>V</s>").replace("v", "<s>V</s>")
        await message.delete(text)
        await message.reply_text(text, quote=False)
    elif value == "modetwo":
        text = message.text.replace("з", "<s>Z</s>").replace("в", "<s>V</s>").replace("З", "<s>Z</s>").replace("В", "<s>V</s>").replace("Z", "<s>Z</s>").replace("z", "<s>Z</s>").replace("V", "<s>V</s>").replace("v", "<s>V</s>")
        await message.edit(
            f"{text}"
            f" 🇺🇦"
        )
        
made_by = f"{channel} | {creator} | {website}"
