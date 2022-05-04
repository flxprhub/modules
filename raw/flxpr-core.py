import os

from aiofile import async_open as open

from helper import module, Message, session
from helper.module import unload_module
from helper.misc import modules_dict

from modules.updater import restart

core_title = "flxpr-core"
core_cmds = ["flxpr-core", "core", "fcore", "fc"]
core_args = ["без аргументов"]
core_desc = "без описания"

loader_title = "flxpr-loader"
loader_cmds = ["flxpr-loader", "loader", "floader", "fl"]
loader_args = ["модуль к установке"]
loader_desc = "без описания"

updater_title = "flxpr-updater"
updater_cmds = ["flxpr-updater", "updater", "fupdater", "fupd"]
updater_args = ["модуль к обновлению"]
updater_desc = "без описания"

unloader_title = "flxpr-unloader"
unloader_cmds = ["flxpr-unloader", "unloader", "funloader", "fu"]
unloader_args = ["модуль к деинсталляции"]
unloader_desc = "без описания"

creator = "@flxpr"
channel = "@flxpr_modules"
website = "flxpr.ru/modules"
version = "2.1.0"


@module(
    cmds=core_cmds,
    args=core_args,
    desc=core_desc
)

async def core(_, message: Message):
    await message.edit(
        f"<b>{core_title}</b>"
        f"\n\n<b>Версия</b>: <code>{version}</code>"
        f"\n\n<b>Канал с модулями</b>: {channel}"
        f"\n\n<b>Прочая информация о модуле</b>: <code>,h flxpr-core</code>",
        disable_web_page_preview=True
    )


@module(
    cmds=loader_cmds,
    args=loader_args,
    desc=loader_desc
)

async def loader(_, message: Message):
    try:
        name = message.command[1].split("/")[-1].replace(".py", "")

        await message.edit(
            f"<b>{loader_title}</b>" f"\n\n<i>Устанавливаю модуль</i> <code>{name}</code>"
        )

        if modules_dict.module_in(f"custom.{name}"):
            await message.edit(
                f"<b>{loader_title}</b>"
                f"\n\n<i>Модуль уже был установлен ранее, используйте</i> <code>,fupd {name}</code> <i>для его обновления</i>"
            )
            return

        async with session.get(
            f"https://modules.flxpr.ml/raw/{name}.py"
        ) as response:
            if not response.ok:
                await message.edit(
                    f"<b>{loader_title}</b>"
                    f"\n\n<i>Модуль не найден</i>"
                )
                return
            else:
                data = await response.read()

        async with open(f"custom/{name}.py", "wb") as f:
            await message.edit(
                f"<b>{loader_title}</b>" f"\n\n<i>Модуль найден, устанавливаю</i>"
            )

            await f.write(data)

            await message.edit(
                f"<b>{loader_title}</b>"
                f"\n\n<i>Модуль</i> <code>{name}</code> <i>установлен</i>"
                f"\n<i>Бот будет перезагружен для применения изменений, при старте вы будете оповещены</i>"
            )
            restart(message, "restart")
    except IndexError:
        await message.edit(
            f"<b>{core_title}</b>"
            f"\n\n<i>Не указан один из</i> <b>обязательных</b> <i>параметров</i>"
        )


@module(
    cmds=updater_cmds,
    args=updater_args,
    desc=updater_desc
)

async def updater(_, message: Message):
    try:
        name = message.command[1].split("/")[-1].replace(".py", "")

        await message.edit(
            f"<b>{updater_title}</b>"
            f"\n\n<i>Начинаю обновление модуля</i> <b>{name}</b>"
        )

        if not modules_dict.module_in(f"custom.{name}"):
            await message.edit(
                f"<b>{updater_title}</b>"
                f"\n\n<i>Модуль не был установлен ранее, используйте</i> <code>,fl {name}</code> <i>для его установки</i>"
            )
            return

        async with session.get(
            f"https://modules.flxpr.ml/raw/{name}.py"
        ) as response:
            if not response.ok:
                await message.edit(
                    f"<b>{loader_title}</b>"
                    f"\n\n<i>Модуль не найден</i>"
                )
                return
            else:
                data = await response.read()

        async with open(f"custom/{name}.py", "wb") as f:
            await message.edit(
                f"<b>{updater_title}</b>" 
                f"\n\n<i>Модуль найден,</i> <b>обновляю</b>"
            )
            await f.write(data)

            await message.edit(
                f"<b>{updater_title}</b>" 
                f"\n\n<i>Модуль</i> <code>{name}</code> <i>обновлен</i>"
                f"\n<i>Бот будет перезагружен для применения изменений, при старте вы будете оповещены</i>"
            )
            restart(message, "restart")
    except IndexError:
        await message.edit(
            f"<b>{core_title}</b>"
            f"\n\n<i>Не указан один из</i> <b>обязательных</b> <i>параметров</i>"
        )


@module(
    cmds=unloader_cmds,
    args=unloader_args,
    desc=unloader_desc
)

async def unloader(_, message: Message):
    try:
        name = message.command[1].split("/")[-1].replace(".py", "")

        await message.edit(
            f"<b>{unloader_title}</b>" f"\n\n<i>Начинаю удаление модуля</i> <b>{name}</b>"
        )

        if name + ".py" not in os.listdir("custom"):
            await message.edit(f"<b>{unloader_title}</b>" f"\n\n<i>Указанный модуль не найден</i>")
            return

        os.remove(f"custom/{name}.py")
        await unload_module(f"custom.{name}")
        await message.edit(
            f"<b>{unloader_title}</b>" f"\n\n<i>Модуль</i> <b>{name}</b> <i>успешно удален</i>"
        )

        restart(message, "restart")
    except IndexError:
        await message.edit(
            f"<b>{core_title}</b>"
            f"\n\n<i>Не указан один из</i> <b>обязательных</b> <i>параметров</i>"
        )


made_by = f"{channel} | {creator} | {website}"
