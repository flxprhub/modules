from helper import module, Message, db

coreTitle = "flxpr-core"
moduleTitle = "database"

commands = ["db", "database"]
arguments = ["set/get/remove", "string", "any"]
description = "модуль для управления базой данных юзербота"

channel = "@flxpr_modules"
creator = "@flxpr"
website = "flxpr.ml"

@module(cmds=commands, args=arguments, description=description)
async def database(_, message: Message):
    try:
        method = message.command[1]
        value = message.command[2]
        if method == "set": insert = message.command[3]
        
        if method == "set":
            db.set(value, insert)
            await message.edit(
                f"<b>{moduleTitle}</b>"
                f"\n\n<i>Параметру</i> <code>{value}</code> <i>присвоено значение</i> <code>{insert}</code>"
            )
        elif method == "get":
            getvalue = db.get(value)
            await message.edit(
                f"<b>{moduleTitle}</b>"
                f"\n\n<i>Параметр</i> <code>{value}</code> <i>имеет значение</i> <code>{getvalue}</code>"
            )
        elif method == "remove":
            db.remove(value)
            await message.edit(
                f"<b>{moduleTitle}</b>"
                f"\n\n<i>Параметр</i> <code>{value}</code> <i>лишён значения</i>"
            )
    except IndexError:
        await message.edit(
           f"<b>{coreTitle}</b>"
           f"\n\n<i>Не указан один из</i> <b>обязательных</b> <i>параметров</i>"
       )
    
made_by = f"{channel} | {creator} | {website}"
