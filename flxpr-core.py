import os
import sys

from aiofile import async_open as open

from helper import module, Message, db, session
from helper.module import load_module, unload_module, all_off_modules
from helper.misc import modules_dict

from modules.updater import restart

coreTitle = "flxpr-core"
coreCommands = ["flxpr-core", "core", "fcore", "fc"]
coreArguments = ["без аргументов"]
coreDescription = "без описания"

loaderTitle = "flxpr-loader"
loaderCommands = ["flxpr-loader", "loader", "floader", "fl"]
loaderArguments = ["модуль к установке"]
loaderDescription = "без описания"

updaterTitle = "flxpr-updater"
updaterCommands = ["flxpr-updater", "updater", "fupdater", "fupd"]
updaterArguments = ["модуль к обновлению"]
updaterDescription = "без описания"

unloaderTitle = "flxpr-unloader"
unloaderCommands = ["flxpr-unloader", "unloader", "funloader", "fu"]
unloaderArguments = ["модуль к деинсталляции"]
unloaderDescription = "без описания"

defaultInfo = "не указана"

"""
repository = "<a href='https://github.com/flxprhub/modules'>flxprhub/modules</a>"
channel = "<a href='https://t.me/flxpr_modules>flxpr-modules</a>"
creator = "<a href='https://t.me/flxpr'>vadim</a>"
website = "<a href='https://flxpr.ru/modules'>flxpr.ru</a>"
version = "1.0.0"
env = "production"
"""

repository = "github.com/flxprhub/modules"
creator = "@flxpr"
channel = "@flxpr_modules"
website = "flxpr.ru/modules"
version = "1.1.1"
# env = "production"


@module(cmds=coreCommands, args=coreArguments, description=coreDescription)
async def core_cmd(_, message: Message):
    try:
        await message.edit(
            f"<b>{coreTitle}</b>"
            f"\n\nВерсия: <code>{version}</code>"
            f"\n\nКанал с модулями: <b>{channel}</b>"
            f"\nРепозиторий на <b>GitHub'е</b>: <b>{repository}</b>"
            f"\n\nПрочее (список команд итп): <code>,h flxpr-core</code>"
        )
    except IndexError:
        await message.edit(
            f"<b>{coreTitle}</b>"
            f"\n\nНе указан один из <b>обязательных</b> параметров"
        )


@module(cmds=loaderCommands, args=loaderArguments, description=loaderDescription)
async def loader_cmd(_, message: Message):
    try:
        name = message.command[1].split("/")[-1].replace(".py", "")

        await message.edit(
            f"<b>{loaderTitle}</b>"
            f"\n\nНачинаю установку модуля <b>{name}</b>"
        )

        await message.edit(
            f"<b>{loaderTitle}</b>" f"\n\nУстанавливаю модуль <b>{name}</b>"
        )

        if f"custom.{name}" in modules_dict.deleted or modules_dict.module_in(
            f"custom.{name}"
        ):
            await message.edit(
                f"<b>{loaderTitle}</b>"
                f"\n\nМодуль уже был установлен ранее, используйте <code>,fupd {name}</code> для его обновления"
            )

            return

        async with session.get(
            f"https://raw.githubusercontent.com/flxprhub/modules/master/{name}.py"
        ) as response:
            if not response.ok:
                await message.edit(
                    f"<b>{loaderTitle}</b>"
                    f"\n\nДанного модуля нет в репозитории на <b>GitHub'е</b>"
                )
                return
            else:
                data = await response.read()

        async with open(f"custom/{name}.py", "wb") as f:
            await message.edit(
                f"<b>{loaderTitle}</b>" f"\n\nМодуль найден, устанавливаю"
            )

            await f.write(data)

            await message.edit(
                f"<b>{loaderTitle}</b>"
                f"\n\nУстановка прошла <b>успешно</b>"
                f"\n<b>Спасибо</b> за использование моих модулей"
            )
            restart(message, "restart")
    except IndexError:
        await message.edit(
            f"<b>{coreTitle}</b>"
            f"\n\nНе указан один из <b>обязательных</b> параметров"
        )


@module(cmds=updaterCommands, args=updaterArguments, description=updaterDescription)
async def updater_cmd(_, message: Message):
    try:
        name = message.command[1].split("/")[-1].replace(".py", "")

        await message.edit(
            f"<b>{updaterTitle}</b>"
            f"\n\nНачинаю обновление модуля <b>{name}</b>"
        )

        '''
        if f"custom.{name}" in modules_dict.deleted or modules_dict.module_in(
            f"custom.{name}"
        ):
            await message.edit(
                f"<b>{updaterTitle}</b>"
                f"\n\nМодуль не был установлен ранее, используйте <code>,fl {name}</code> для его установки"
            )
            return
        '''

        async with session.get(
            f"https://raw.githubusercontent.com/flxprhub/modules/master/{name}.py"
        ) as response:
            if not response.ok:
                await message.edit(
                    f"<b>{loaderTitle}</b>"
                    f"\n\nДанного модуля нет в репозитории на <b>GitHub'е</b>"
                )
                return
            else:
                data = await response.read()

        async with open(f"custom/{name}.py", "wb") as f:
            await message.edit(
                f"<b>{updaterTitle}</b>" f"\n\nМодуль найден, <b>обновляю</b>"
            )
            await f.write(data)

            await message.edit(
                f"<b>{updaterTitle}</b>" f"\n\nМодуль обновлен, <b>спасибо</b> за использование моих модулей!"
            )
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
            f"<b>{unloaderTitle}</b>" f"\n\nНачинаю удаление модуля <b>{name}</b>"
        )

        if name + ".py" not in os.listdir("custom"):
            await message.edit(f"<b>{unloaderTitle}</b>" f"\n\nМодуль не найден")
            return

        os.remove(f"custom/{name}.py")
        await unload_module(f"custom.{name}")
        await message.edit(
            f"<b>{unloaderTitle}</b>" f"\n\nМодуль <b>{name}</b> успешно удален"
        )

    #        restart(message, "restart")
    except IndexError:
        await message.edit(
            f"<b>{coreTitle}</b>"
            f"\n\nНе указан один из <b>обязательных</b> параметров"
        )


made_by = f"{channel} | {creator} | {website}"
