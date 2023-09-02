from bot import Bot


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
if token is None:
    print("Failed to parse a token from 'token.key' file.")
    exit(-1)

bot = Bot(token)
bot.run()
