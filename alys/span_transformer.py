from alys.lexer import Lexer
from alys.token import Token
import re

pattern_dict = {
    "italics_pattern": r"(\*.*?\*)|(_.*?_)",
    "bold_pattern": r"(\*\*.*?\*\*)|(__.*?__)",
    "strikethrough_pattern": r"~~.*?~~",
    "link_pattern": r"\[.*?\]\(.*?\)",
    "image_pattern": r"!\[.*?\]\(.*?\)",
    "code_pattern": r"`.*?`",
}


class SpanTransformer:
    def __init__(self, lexer: Lexer) -> None:
        self.tokens = lexer.tokens

    def transform_spans(self, token: Token):
        if not self.is_span(token.content):
            return
        original = token.content
        transformed = self.transform(original)
        while original != transformed:
            original = transformed
            transformed = self.transform(original)
        token.content = transformed

    def transform(self, line: str) -> str:
        line = self.handle_bold(line)
        line = self.handle_italics(line)
        line = self.handle_strikethrough(line)
        line = self.handle_img(line)
        line = self.handle_link(line)
        line = self.handle_code(line)
        return line

    def span_match(self, line: str) -> re.Match[str] | None:
        combined_pattern = "|".join([pattern_dict[p] for p in pattern_dict])
        match = re.search(combined_pattern, line)
        return match

    def is_span(self, line: str) -> bool:
        return bool(self.span_match(line))

    def span_pos(self, line: str) -> tuple[int, int]:
        match = self.span_match(line)
        if match is not None:
            return match.span()
        return (-1, -1)

    def handle_italics(self, line: str) -> str:
        italics_pattern = re.compile(rf"{pattern_dict['italics_pattern']}")

        def replacer(m: re.Match):
            inner = m.group(1) or m.group(2)
            inner = inner[1:-1]
            inner = self.handle_italics(inner)
            return f"<i>{inner}</i>"

        return italics_pattern.sub(replacer, line)

    def handle_bold(self, line: str) -> str:
        bold_pattern = re.compile(rf"{pattern_dict['bold_pattern']}")

        def replacer(m):
            inner = m.group(1) or m.group(2)
            inner = inner[2:-2]
            inner = self.handle_bold(inner)
            return f"<b>{inner}</b>"

        return bold_pattern.sub(replacer, line)

    def handle_strikethrough(self, line: str) -> str:
        strikethrough_pattern = re.compile(rf"{pattern_dict['strikethrough_pattern']}")
        return strikethrough_pattern.sub(lambda x: f"<s>{x.group()[2:-2]}</s>", line)

    def handle_link(self, line: str) -> str:
        link_pattern = re.compile(rf"{pattern_dict['link_pattern']}")
        return link_pattern.sub(
            lambda x: f'<a href="{x.group()[1:-1].split("](")[1]}">{x.group()[1:-1].split("](")[0]}</a>',
            line,
        )

    def handle_img(self, line: str) -> str:
        image_pattern = re.compile(rf"{pattern_dict['image_pattern']}")
        return image_pattern.sub(
            lambda x: f'<img src="{x.group()[2:-1].split("](")[1]}" alt="{x.group()[2:-2].split("](")[0]}"/>',
            line,
        )

    def handle_code(self, line: str) -> str:
        code_pattern = re.compile(rf"{pattern_dict['code_pattern']}")
        return code_pattern.sub(lambda x: f"<code>{x.group()[1:-1]}</code>", line)
