import sys
import unittest

sys.path.insert(0, "..")
from alys import lexer


class TestLexer(unittest.TestCase):
    def test_atx_heading(self):
        test_cases = [
            ("# h1", lexer.Token(lexer.Tag.H1, "h1")),
            ("# # h1", lexer.Token(lexer.Tag.H1, "# h1")),
            ("# # h1 #################", lexer.Token(lexer.Tag.H1, "# h1")),
            ("## h2", lexer.Token(lexer.Tag.H2, "h2")),
            ("##h2", lexer.Token(lexer.Tag.P, "##h2")),
            ("### h3", lexer.Token(lexer.Tag.H3, "h3")),
            ("#### h4", lexer.Token(lexer.Tag.H5, "h4")),
            ("##### h5", lexer.Token(lexer.Tag.H5, "h5")),
            ("###### h6", lexer.Token(lexer.Tag.H6, "h6")),
            ("####### p", lexer.Token(lexer.Tag.P, "####### p")),
            ("## p ###", lexer.Token(lexer.Tag.H2, "p")),
            ("## p #################", lexer.Token(lexer.Tag.H2, "p")),
            ("## p # ################", lexer.Token(lexer.Tag.H2, "p #")),
            ("## p # ################        ", lexer.Token(lexer.Tag.H2, "p #")),
        ]

        for test_case in test_cases:
            l = lexer.Lexer()
            text = test_case[0]
            want = test_case[1]
            l.lex(text)
            got = l.get_latest_token()
            self.assertEqual(got.content, want.content)

    def test_is_setext(self):
        test_cases = [
            ("-", True),
            ("- ", True),
            ("=       ", True),
            ("===========        ", True),
            ("------- ", True),
            ("=", True),
            ("===========", True),
            ("-------", True),
            ("-====", False),
            (" ====", False),
            ("==Hello==", False),
            ("---Hello--", False),
            ("== ==", False),
            (" -", False),
            ("- -", False),
            (" =", False),
        ]

        for test_case in test_cases:
            l = lexer.Lexer()
            text = test_case[0]
            want = test_case[1]
            got = l.is_setext(text)
            self.assertEqual(got, want)

    def test_setext_heading(self):
        test_cases = [
            ("h1", "=", lexer.Token(lexer.Tag.H1, "h1")),
            ("h2", "-", lexer.Token(lexer.Tag.H2, "h2")),
            ("h1", "==============", lexer.Token(lexer.Tag.H1, "h1")),
            ("h2", "--------", lexer.Token(lexer.Tag.H2, "h2")),
        ]

        for test_case in test_cases:
            l = lexer.Lexer()
            above = test_case[0]
            below = test_case[1]
            want = test_case[2]
            l.lex(above)
            l.lex(below)
            got = l.get_latest_token()
            self.assertEqual(got.content, want.content)


if __name__ == "__main__":
    unittest.main()