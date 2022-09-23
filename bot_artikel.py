from aiogram import Bot, types, Dispatcher, executor
from config import bot_token, openWeatherApiKey
import requests
from bs4 import BeautifulSoup
import re

bot = Bot(token=bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.reply("Hi! I'm ArtikelBot. Send me a noun!")


@dp.message_handler()
async def getWord(message: types.Message):
    inp_word = message.text
    word = inp_word.capitalize()

    def check(word):
        check_der = requests.get('https://der-artikel.de/der/'+word+'.html')
        check_das = requests.get('https://der-artikel.de/das/'+word+'.html')
        check_die = requests.get('https://der-artikel.de/die/'+word+'.html')
        if check_der:
            return "der"
        elif check_das:
            return "das"
        elif check_die:
            return "die"
        else:
            return None

    if check(word) == None:
        await message.reply("Sorry, I don't know this word :(")
    else:
        await message.reply(check(word)+" "+word)

    def check_art():
        if check(word) == "der":
            return 'https://der-artikel.de/der/'+word+'.html'
        elif check(word) == "das":
            return 'https://der-artikel.de/das/'+word+'.html'
        elif check(word) == "die":
            return 'https://der-artikel.de/die/'+word+'.html'
        else:
            return None

    def translateToEnglish():
        url = check_art()
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        element = soup.find("h3", class_="mb-5")
        form_el = element.text.strip()
        el = re.split('\W+', form_el)
        trnsl = el[-1]
        return ("eng: "+trnsl)

    await message.reply(translateToEnglish())


executor.start_polling(dp)
