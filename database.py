from helper import module, Message, db

@module(cmds=["db", "database"], args=["set/get/remove", "string", "any"], description="модуль для управления базой данных юзербота")
async def database(_, message: Message):
    try:
        method = message.text.split(maxsplit=-1)[1]
        value = message.text.split(maxsplit=-1)[2]
        if method == "set": insert = message.text.split(maxsplit=-1)[3]
        if method == "set":
            db.set(value, insert)
            await message.edit(f"<b>DB</b> / Параметру <b>{value}</b> присвоено значение <b>{insert}</b>")
        elif method == "get":
            getvalue = db.get(value)
            await message.edit(f"<b>DB</b> / Параметр <b>{value}</b> имеет значение <b>{getvalue}</b>")
        elif method == "remove":
            db.remove(value)
            await message.edit(f"<b>DB</b> / Параметр <b>{value}</b> лишён значения")
    except IndexError:
        await message.edit(f"<b>DB</b> / Не указан один из  <b>обязательных</b> параметров")
    
made_by = "@flxpr"
other_info = "flxpr.ru"