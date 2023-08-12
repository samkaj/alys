from alys.token import Tag, Token


class Lexer:
    def __init__(self) -> None:
        self.tokens = []
        self.current_tag = Tag.HTML

    def add(self, token: Token):
        self.tokens.append(token)

    def lex(self, line: str):
        if self.is_atx(line):
            self.handle_atx_heading(line)
            return
        if self.is_setext(line):
            self.handle_setext_heading(line)
            return
        if self.is_list_item(line):
            self.handle_list(line)
            return
        self.paragraph(line)

    def set_current_tag(self, new_tag: Tag):
        self.current_tag = new_tag

    def get_tokens(self) -> list[Token]:
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

    def handle_setext_heading(self, line: str) -> None:
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

    def handle_atx_heading(self, line: str) -> None:
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

    def is_list_item(self, line: str) -> bool:
        line = line.lstrip()
        if line.startswith("- ") or line.startswith("* "):
            return True

        ordered = line.split(".")
        if len(ordered) < 2:
            return False

        for c in ordered[0]:
            if c not in "1234567890":
                return False

        return ordered[1].startswith(" ")

    def handle_list(self, line: str):
        if not self.is_list_item(line):
            raise TypeError(f'expected a list item ("n. ", "- ", or "* "), got {line}')

        is_unordered = line.startswith("-") or line.startswith("*")
        idents = 0
        offset = 0

        if is_unordered:
            content = line.lstrip()[1:]
        else:
            for c in line.lstrip():
                if c == ".":
                    offset += 1
                    break

        for c in line:
            if c == " ":
                idents += 1
                continue
            break

        for _ in range(idents // 2):
            self.add(Token(Tag.IDENT))

        content = line[idents + offset + 2 :]

        self.add(Token(Tag.LI, content))
