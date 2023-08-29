import telebot
from messages import START_MESSAGE


def parse_token(filename: str = "token.key") -> str | None:
    token = None
    try:
        with open(filename) as token_file:
            content = token_file.read()
            token = content.strip()
            return token
    except Exception:
        return None


token = parse_token()
if token is not None:
    bot = telebot.TeleBot(token)
else:
    print("Failed to parse a token from 'token.key' file.")
    exit(-1)


@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.from_user.id
    bot.send_message(user_id, START_MESSAGE, parse_mode="Markdown")


bot.polling(none_stop=True, interval=0)
