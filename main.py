import os
import logging
import asyncio
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ParseMode
from dotenv import load_dotenv
from helper import Helper

logging.basicConfig(level=logging.INFO)

load_dotenv()
TOKEN = os.getenv("TOKEN")
PASHKA = int(os.getenv("PASHKA"))
ME = int(os.getenv("ME"))
bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot)
TOTAL = "0"


async def scheduled(wait_for, searcher):
    while True:
        await searcher()
        await asyncio.sleep(wait_for)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    print(message)
    if message.from_user.id == PASHKA:
        await message.answer("Здарова, Пашка")
    else:
        await message.answer("Бот не для тебя, ты не Пашка Ковальчук")


async def search_count():
    global TOTAL
    s = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s)
    page = Helper(driver)
    page.go_to_site()
    element = page.find_count()
    last_operation = element.text.split("\n")[0].split()
    date = f"{last_operation[1]} - {last_operation[2]}"
    change_count = f"{last_operation[3]}{last_operation[4]}"
    rate = last_operation[-2]
    total_amount = f"{last_operation[7]}"
    text = f"{date}\n{change_count}\n{rate}"
    if total_amount != TOTAL:
        await bot.send_message(chat_id=PASHKA, text=text)
        await bot.send_message(chat_id=ME, text=text)
        TOTAL = total_amount
    return True


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(scheduled(360, search_count))
    executor.start_polling(dp, skip_updates=True)
