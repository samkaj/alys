from alys.token import Tag, Token


class Lexer:
    def __init__(self) -> None:
        self.tokens = []

    def add(self, token: Token):
        self.tokens.append(token)

    def lex(self, line: str):
        if self.is_atx(line):
            self.atx_heading(line)
            return
        if self.is_setext(line):
            self.setext_heading(line)
            return
        self.paragraph(line)

    def get_tokens(self):
        return self.tokens

    def get_latest_token(self) -> Token:
        return self.tokens[-1]

    def is_setext(self, line: str) -> bool:
        if len(line) < 1:
            return False
        c = line[0]
        return line.startswith(c) and line.strip().replace(c, "") == ""

    def is_atx(self, line: str) -> bool:
        if not line.startswith("#"):
            return False

        max_heading_level = 6
        i = 0
        current_char = line[i]
        while current_char in "# ":
            if i > max_heading_level:
                return False
            if current_char == " ":
                break
            i += 1
            current_char = line[i]

        return current_char == " "

    def set_latest_token(self, token: Token) -> None:
        self.tokens[-1] = token

    def paragraph(self, line: str) -> None:
        self.add(Token(Tag.P, line))

    def setext_heading(self, line: str) -> None:
        if not self.is_setext(line):
            raise TypeError(
                f'invalid setext line, expected exclusively at least one "=" or "-", got {line}'
            )

        token_above = self.get_latest_token()
        if token_above.tag != Tag.P:
            self.add(Token(Tag.P, line))
            return

        tag = Tag.H1
        if line.startswith("-"):
            tag = Tag.H2

        self.set_latest_token(Token(tag, token_above.content))

    def atx_heading(self, line: str) -> None:
        if not line.startswith("#"):
            raise TypeError(f"invalid header prefix, got {line}")

        line = line.rstrip()

        level = 0
        for c in line:
            if c == "#":
                level += 1
                continue
            break

        trailing_hashes = 0
        for c in reversed(line):
            if c == "#":
                trailing_hashes += 1
                continue
            break

        content = line[level + 1 : len(line) - trailing_hashes].strip()

        match level:
            case 1:
                token = Token(Tag.H1, content)
            case 2:
                token = Token(Tag.H2, content)
            case 3:
                token = Token(Tag.H3, content)
            case 4:
                token = Token(Tag.H4, content)
            case 5:
                token = Token(Tag.H5, content)
            case 6:
                token = Token(Tag.H6, content)
            case _:
                token = Token(Tag.P, line)

        self.add(token)
