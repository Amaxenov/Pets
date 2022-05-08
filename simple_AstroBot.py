# Astro-echo-bota

import ephem
import logging
import settings

from datetime import date
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


logging.basicConfig(filename='my_bot.log', level=logging.INFO)


def greet_user(update, context):
    print()
    print('Pressed /start in TestBot')
    update.message.reply_text('Hi, new user!')
    print()
    print(update)


def planet_constellation(update, context):
    user_text = update.message.text
    user_text = user_text.split()
    user_planet = user_text[-1]
    what_day_today = date.today().strftime('%Y/%m/%d')
    
    # What planet the user need.
    if user_planet == 'Mars':
        planet = ephem.Mars()
    elif user_planet == 'Mercury':
        planet = ephem.Mercury()
    elif user_planet == 'Venus':
        planet = ephem.Venus()
    elif user_planet == 'Jupiter':
        planet = ephem.Jupiter()
    elif user_planet == 'Saturn':
        planet = ephem.Saturn()
    elif user_planet == 'Uranus':
        planet = ephem.Uranus()
    elif user_planet == 'Neptune':
        planet = ephem.Neptune()
    else:
        update.message.reply_text(f'Укажите название планеты после команды /planet  '
                                                                'Список планет: Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune')
    
    # What constellation today for chosen planet.    
    planet.compute(what_day_today)
    constellation = ephem.constellation(planet)
    update.message.reply_text(f'{user_planet} сегодня находится в созвездии {constellation}')


# Echo.
def talk_to_me(update, context):
    user_text = update.message.text
    print(user_text)
    update.message.reply_text(user_text)


def main():
    my_bot = Updater(settings.API_KEY, use_context=True)

    dp = my_bot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('planet', planet_constellation))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info('TestBot started.')
    my_bot.start_polling()
    my_bot.idle()


if __name__ == '__main__':
    main()
