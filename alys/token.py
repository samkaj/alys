from enum import Enum

Tag = Enum(
    "Tag",
    [
        "HTML",
        "P",
        "H1",
        "H2",
        "H3",
        "H4",
        "H5",
        "H6",
        "UL",
        "OL",
        "LI",
        "EMPTY",
        "IDENT",
        "HR",
    ],
)


class Token:
    def __init__(self, tag: Tag, content: str = "") -> None:
        self.tag = tag
        self.content = content

    def __str__(self) -> str:
        content = ""
        if len(self.content):
            content = f"({self.content})"
        return f"{str(self.tag)}{content}"
