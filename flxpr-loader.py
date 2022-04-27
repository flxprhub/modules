import os
import sys

from aiofile import async_open as open

from helper import module, Message, db, session
from helper.module import load_module, unload_module, all_off_modules

coreTitle = "flxpr-core"
coreCommands = ["flxpr-core", "core", "fcore", "fc"]
coreArguments = ["без аргументов"]
coreDescription = "без описания"

loaderTitle = "flxpr-loader"
loaderCommands = ["flxpr-loader", "loader","floader", "fl"]
loaderArguments = ["модуль к установке"]
loaderDescription = "без описания"

unloaderTitle = "flxpr-unloader"
unloaderCommands = ["flxpr-unloader", "unloader", "funloader", "fu"]
unloaderArguments = ["модуль к деинсталляции"]
unloaderDescription = "без описания"

defaultInfo = "не указана"

repository = "https://raw.githubusercontent.com/flxprhub/modules/main/lib"
channel = "@flxpr_modules"
creator = "@flxpr"
website = "flxpr.ru/modules"
version = "0.2.2"

def restart(message: Message, restart_type):
    text = "1" if restart_type == "update" else "2"
    os.execvp(
        sys.executable,
        [
            sys.executable,
            "run.py",
            f"{message.chat.id}",
            f" {message.id}",
            f"{text}",
        ],
    )

@module(cmds=coreCommands, args=coreArguments, description=coreDescription)
async def core_cmd(_, message: Message):
    try:
        await message.edit(
            f"<b>{coreTitle}</b>"
            f"\n\nВерсия: <code>{version}</code>"
            f"\nКанал с модулями: {channel}"
            f"\nСоздатель: {creator}"
            f"\nВеб-сайт: {website}"
        )
    except IndexError:
       await message.edit(
           f"<b>{coreTitle}</b>"
           f"\n\nНе указан один из <b>обязательных</b> параметров"
       )

@module(cmds=loaderCommands, args=loaderArguments, description=loaderDescription)
async def loader_cmd(_, message: Message):
    try:
        name  = message.command[1].split("/")[-1].replace(".py", "")
        link = session.get(f"https://raw.githubusercontent.com/flxprhub/modules/{name}")
        
        await message.edit(
             f"<b>{loaderTitle}</b>" 
             f"\n\nНачинаю установку модуля <b>{name}</b>"
             f"\n<b>⚡ Дополнительная информация</b>: {defaultInfo}"
        )
        
        await message.edit(
            f"<b>{loaderTitle}</b>"
            f"\n\nУстанавливаю модуль <b>{name}</b>"
        )
        
        async with link as response:
            if response.status != 200:
                await message.edit(
                    f"<b>{loaderTitle}</b>"
                    f"\n\nДанного модуля нет в репозитории на <b>GitHub'е</b>"
                )
                return
                
        async with open(f"custom/{name}.py", "wb") as f:
            await f.write(await response.read())
            load_module(f"custom.{name}")
            restart(message, "restart")
    except IndexError:
       await message.edit(
           f"<b>{coreTitle}</b>"
           f"\n\nНе указан один из <b>обязательных</b> параметров"
       )
       
@module(cmds=unloaderCommands, args=unloaderArguments, description=unloaderDescription)

async def unloader_cmd(_, message: Message):
    try:
        name = message.command[1].split("/")[-1].replace(".py", "")
        
        await message.edit(
            f"<b>{unloaderTitle}</b>"
            f"\n\nНачинаю удаление модуля <b>{name}</b>"
        )
        
        if name + ".py" not in os.listdir("custom"):
            await message.edit(
                f"<b>{unloaderTitle}</b>"
                f"\n\nМодуль не найден"
            )
            return
        
        os.remove(f"custom/{name}.py")
        await unload_module(f"custom.{name}")
        await message.edit(
            f"<b>{unloaderTitle}</b>"
            f"\n\nМодуль <b>{name}</b> успешно удален"
        )
        
        restart(message, "restart")
    except IndexError:
       await message.edit(
           f"<b>{coreTitle}</b>"
           f"\n\nНе указан один из <b>обязательных</b> параметров"
       )
       
made_by = f"{channel} | {creator} | {website}"