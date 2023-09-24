import sys
import unittest
from alys import lexer

from alys.token import Token, Tag

sys.path.insert(0, "..")
from alys.span_transformer import SpanTransformer


class TestSpanTransformer(unittest.TestCase):
    def test_is_span(self):
        span_helper = lambda c: f"hello {c} world {c}"

        matching_tokens = [
            Token(Tag.H1, span_helper("*")),
            Token(Tag.H1, span_helper("**")),
            Token(Tag.H1, span_helper("`")),
            Token(Tag.H1, span_helper("~~")),
            Token(Tag.H1, span_helper("__")),
            Token(Tag.P, "![an image](#)"),
            Token(Tag.P, "[a link](#)"),
            Token(Tag.H1, span_helper("***")),
            Token(Tag.H1, span_helper("__*")),
        ]
        l = lexer.Lexer()
        l.tokens = matching_tokens
        s = SpanTransformer(l)
        for token in s.tokens:
            self.assertEqual(s.is_span(token.content), True)

    def test_is_not_span(self):
        not_matching_tokens = [
            Token(Tag.P, "![an image(]#)"),
            Token(Tag.P, "(not a link)[#]"),
            Token(Tag.H1, "*hello~"),
            Token(Tag.H1, "~ ~hello~~"),
        ]
        l = lexer.Lexer()
        l.tokens = not_matching_tokens
        s = SpanTransformer(l)
        for token in s.tokens:
            self.assertEqual(s.is_span(token.content), False)

    def test_transform(self):
        test_cases = [
            ("*italic*", lexer.Token(lexer.Tag.P, "<i>italic</i>")),
            ("**bold**", lexer.Token(lexer.Tag.P, "<b>bold</b>")),
            ("~~strikethrough~~", lexer.Token(lexer.Tag.P, "<s>strikethrough</s>")),
            ("[link](url)", lexer.Token(lexer.Tag.P, '<a href="url">link</a>')),
            ("![alt](url)", lexer.Token(lexer.Tag.P, '<img src="url" alt="alt"/>')),
            ("`code`", lexer.Token(lexer.Tag.P, "<code>code</code>")),
            (
                "**nested *italic* bold**",
                lexer.Token(lexer.Tag.P, "<b>nested <i>italic</i> bold</b>"),
            ),
            ("no_formatting", lexer.Token(lexer.Tag.P, "no_formatting")),
        ]

        for test_case in test_cases:
            l = lexer.Lexer()
            text = test_case[0]
            want = test_case[1]
            l.lex(text)
            s = SpanTransformer(l) 
            s.transform_spans(l.get_latest_token())
            got = l.get_latest_token()
            self.assertEqual(got.content, want.content)
