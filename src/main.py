from utils import parse_token


token = parse_token()
if token is None:
    print("Failed to parse a token from 'token.key' file.")
    exit(-1)


token_safe: str = token
import bot
