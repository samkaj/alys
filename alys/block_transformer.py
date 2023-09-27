from alys.lexer import Lexer
from alys.token import Tag, Token


class BlockTransformer:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.tokens = lexer.tokens
        self.html = []
    
    def transform(self) -> str:
        for token in self.tokens:
            self.transform_block(token)
    
    def get_html(self) -> str:
        return "\n".join(self.html)
    
    def transform_block(self, token: Token):
        self.handle_heading(token)
        self.handle_paragraph(token)
        self.handle_code_block(token)
        self.handle_blockquote(token)
        self.handle_hr(token)
        self.handle_list(token)
    
    def handle_list(self, token: Token):
        if token.tag == Tag.LI:
            self.html.append(f"<li>{token.content}</li>")
            return
    
    def handle_hr(self, token: Token):
        if token.tag == Tag.HR:
            self.html.append("<hr>")
    
    def handle_blockquote(self, token: Token):
        if token.tag == Tag.BLOCKQUOTE:
            self.html.append(f"<blockquote>{token.content}</blockquote>")
    
    def handle_code_block(self, token: Token):
        if token.tag == Tag.INDENTEDCODE:
            self.html.append(f"<pre><code>{token.content}</code></pre>")

    def handle_paragraph(self, token: Token):
        if token.tag == Tag.P:
            self.html.append(f"<p>{token.content}</p>")
    
    def handle_heading(self, token: Token):
        if token.tag == Tag.H1:
            self.html.append(f"<h1>{token.content}</h1>")
        if token.tag == Tag.H2:
            self.html.append(f"<h2>{token.content}</h2>")
        if token.tag == Tag.H3:
            self.html.append(f"<h3>{token.content}</h3>")
        if token.tag == Tag.H4:
            self.html.append(f"<h4>{token.content}</h4>")
        if token.tag == Tag.H5:
            self.html.append(f"<h5>{token.content}</h5>")
        if token.tag == Tag.H6:
            self.html.append(f"<h6>{token.content}</h6>")
    
        
    