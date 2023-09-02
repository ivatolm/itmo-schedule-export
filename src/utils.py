def parse_token(filename: str = "token.key") -> str | None:
    token = None
    try:
        with open(filename) as token_file:
            content = token_file.read()
            token = content.strip()
            return token
    except Exception:
        return None
