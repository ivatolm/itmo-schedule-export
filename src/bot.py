import telebot
from telebot import types, custom_filters
from telebot.handler_backends import State, StatesGroup
from telebot.storage import StatePickleStorage

import itmo
from messages import (
    START_MESSAGE,
    GET_URL_MESSAGE,
    UNKNOWN_CMD_MESSAGE
)


class BotStates(StatesGroup):
    start = State()
    get_url = State()


class Bot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token,
                                   state_storage=StatePickleStorage())
        self.bot.add_custom_filter(custom_filters.StateFilter(self.bot))

        self.bot.register_message_handler(self.start,
                                          commands=["start"],
                                          pass_bot=True)
        self.bot.register_message_handler(self.proceed_url,
                                          commands=["get_url"],
                                          pass_bot=True)
        self.bot.register_message_handler(self.get_url,
                                          state=BotStates.get_url,
                                          pass_bot=True)

    def run(self):
        self.bot.polling(none_stop=True, interval=0)

    @staticmethod
    def start(message, bot):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        get_url_btn = types.KeyboardButton("/get_url")
        markup.add(get_url_btn)

        bot.send_message(message.chat.id, START_MESSAGE,
                         parse_mode="Markdown", reply_markup=markup)
        bot.set_state(message.from_user.id, BotStates.start, message.chat.id)

    @staticmethod
    def proceed_url(message, bot):
        markup = types.ReplyKeyboardRemove()

        bot.send_message(message.chat.id, GET_URL_MESSAGE, reply_markup=markup)
        bot.set_state(message.from_user.id, BotStates.get_url, message.chat.id)

    @staticmethod
    def get_url(message, bot):
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["auth"] = message.text

        schedule = itmo.fetch_schedule(data["auth"])
        if schedule is None:
            bot.send_message(message.chat.id, UNKNOWN_CMD_MESSAGE)
            return

        itmo.parse_schedule(schedule)
