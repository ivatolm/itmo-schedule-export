import telebot
from telebot import types

from reqs import fetch_schedule
from messages import (
    START_MESSAGE,
    GET_URL_MESSAGE,
    UNKNOWN_CMD_MESSAGE
)


class Bot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)
        self.bot.register_message_handler(self.start,
                                          commands=["start"],
                                          pass_bot=True)
        self.bot.register_message_handler(self.get_url,
                                          commands=["get_url"],
                                          pass_bot=True)
        self.bot.register_message_handler(self.get_text,
                                          content_types=["text"],
                                          pass_bot=True)

    def run(self):
        self.bot.polling(none_stop=True, interval=0)

    @staticmethod
    def start(message, bot):
        user_id = message.from_user.id

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        get_url_btn = types.KeyboardButton("/get_url")
        markup.add(get_url_btn)

        bot.send_message(user_id, START_MESSAGE,
                         parse_mode="Markdown", reply_markup=markup)

    @staticmethod
    def get_url(message, bot):
        user_id = message.from_user.id

        markup = types.ReplyKeyboardRemove()

        bot.send_message(user_id, GET_URL_MESSAGE, reply_markup=markup)

    @staticmethod
    def get_text(message, bot):
        user_id = message.from_user.id

        if not message.text:
            bot.send_message(user_id, UNKNOWN_CMD_MESSAGE)
            return

        auth = message.text
        schedule = fetch_schedule(auth)
        if schedule is None:
            bot.send_message(user_id, UNKNOWN_CMD_MESSAGE)
            return

        for day in schedule:
            date = day["date"]
            pairs = day["lessons"]

            print(date)
            for pair in pairs:
                p_name = pair["subject"]
                p_type = pair["type"]
                p_ts = pair["time_start"]
                p_te = pair["time_end"]
                p_teacher = pair["teacher_name"]

                print(p_name, p_type, p_ts, p_te, p_teacher)
