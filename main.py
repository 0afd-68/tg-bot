from serv import *
import asyncio

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

TOKEN = "7598009708:AAGq_wJcCVRLq3VwGLHs12RYdrDbAtaRKjw"
PREFIXS = ["https","http","ftp","mailto","file","tel"]
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Привет, {html.bold(message.from_user.full_name)}! Это бот для сокращения ссылок, сюда достаточно отправить длинную ссылку, чтобы получить укороченную версию")

@dp.message()
async def handler(message: Message) -> None:
    try:
        text = message.text
        print(text)
        if text == "/stats":
            try:
                a = statists(message.chat.id)
                for i in a:
                    txt =i[0]+"    --     "+i[1]
                    await bot.send_message(chat_id = message.chat.id, text=txt)
            except:
                await bot.send_message(chat_id = message.chat.id, text="у тебя нету истории отправленных ссылок")
        elif text.split(':')[0] in PREFIXS:
            await bot.send_message(chat_id=message.chat.id, text=create_uniqueurl(message.text,str(message.chat.id)))
        else:
            # await bot.send_message(chat_id=message.chat.id,reply_to_message_id= text="Это не ссылка")
            await message.reply("Это не ссылка")
    except TypeError:
        await message.answer("Nice try!")




async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
