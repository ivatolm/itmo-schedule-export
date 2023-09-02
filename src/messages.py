REPO_LINK = "https://github.com/ivatolm/itmo-schedule-export"
MY_ITMO_LINK = "https://my.itmo.ru/"

START_MESSAGE = (
    "Hello, this bot is used to import your itmo schedule into "
    "Google Calendar.\n\n"

    "How does this work?\n"
    f"This is done by downloading it from [my.itmo]({MY_ITMO_LINK})"
    " via cookie you give to this bot. "
    "Beware, that giving cookie gives this bot full access to your account. "
    "If you do not trust it, then you can host your own version of the bot. "
    f"All sources are avaliable at github [repo]({REPO_LINK})"
)

GET_URL_MESSAGE = (
    "Please, send you authorization hash"
)

UNKNOWN_CMD_MESSAGE = (
    "Sorry, but I don't understand this command"
)
