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

    def test_is_list_item(self):
        test_cases = [
            ("- unordered list item", True),
            ("* unordered list item", True),
            ("1. ordered list item", True),
            ("0. ordered list item", True),
            ("0001230532452. ordered list item", True),
            ("  - unordered list item", True),
            ("-list item", False),
            ("*list item", False),
            ("12334.list item", False),
            ("123d3. list item", False),
            ("-- list item", False),
        ]

        for test_case in test_cases:
            l = lexer.Lexer()
            got = l.is_list_item(test_case[0])
            want = test_case[1]
            self.assertEqual(got, want)

    def test_handle_list(self):
        test_cases = [
            ("      - list", 3, lexer.Tag.LI),
            ("       * list", 3, lexer.Tag.LI),
            ("  - list", 1, lexer.Tag.LI),
            ("   1. list", 1, lexer.Tag.LI),
            ("    1. list", 2, lexer.Tag.LI),
            ("      1. list", 3, lexer.Tag.LI),
            ("       1. list", 3, lexer.Tag.LI),
            ("  1. list", 1, lexer.Tag.LI),
            ("   1. list", 1, lexer.Tag.LI),
            ("    1. list", 2, lexer.Tag.LI),
            ("  123452345. list", 1, lexer.Tag.LI),
            ("   3341114576776. list", 1, lexer.Tag.LI),
            ("    11234432. list", 2, lexer.Tag.LI),
            ("    112. 34432. list", 2, lexer.Tag.LI),
            ("  13948579283475. list", 1, lexer.Tag.LI),
            ("   1098098098. list", 1, lexer.Tag.LI),
            ("    11235. list", 2, lexer.Tag.LI),
        ]

        for test_case in test_cases:
            l = lexer.Lexer()
            l.lex(test_case[0])
            want = test_case[2]
            tokens = l.get_tokens()
            j = 0
            if test_case[0].lstrip()[0] in "-*":
                content = "".join(test_case[0].lstrip()[2:])
            else:
                offset = test_case[0].find(". ")
                content = "".join(test_case[0][offset + 2 :])

            for i in range(test_case[1]):
                self.assertEqual(tokens[i].tag, lexer.Tag.IDENT)
                j += 1

            self.assertEqual(tokens[j].tag, want)
            self.assertEqual(tokens[j].content, content)

    def test_is_hr(self):
        test_cases = [
            ("- - -", True),
            ("_ _ _", True),
            ("* * *", True),
            ("***", True),
            ("---", True),
            ("___", True),
            ("      ***", True),
            ("    ---", True),
            ("     ___", True),
            ("*          **", True),
            ("--      -", True),
            ("_  _        _", True),
            ("_____________________", True),
            ("----------------", True),
            ("************", True),
            ("*-**********", False),
            ("****____*******", False),
            ("--------_", False),
            ("*", False),
            ("", False),
            ("--", False),
            ("**", False),
            ("_", False),
            ("-", False),
            ("_", False),
            ("333", False),
            ("33333333333333", False),
            ("aaaaaaaaa", False),
            ("aa", False),
        ]

        for test_case in test_cases:
            l = lexer.Lexer()
            got = l.is_hr(test_case[0])
            want = test_case[1]
            self.assertEqual(got, want)

    def test_br(self):
        test_cases = [
            ("hello world  ", True),
            ("hello world      ", True),
            ("hello world    ", True),
            ("hello world   . ", False),
            ("hello world.", False),
        ]

        for test_case in test_cases:
            l = lexer.Lexer()
            l.lex(test_case[0])
            got = l.get_latest_token().tag == lexer.Tag.BR
            want = test_case[1]
            self.assertEqual(got, want)
            



if __name__ == "__main__":
    unittest.main()
