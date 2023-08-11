from enum import Enum


class Tag(Enum):
    HTML = 0
    P = 1
    H1 = 2
    H2 = 3
    H3 = 4
    H4 = 5
    H5 = 6
    H6 = 7
    EMPTY = 8


class Token:
    def __init__(self, tag: Tag, content: str = "") -> None:
        self.tag = tag
        self.content = content

    def __str__(self) -> str:
        content = ""
        if len(self.content):
            content = f"({self.content})"
        return f"{str(self.tag)}{content}"
