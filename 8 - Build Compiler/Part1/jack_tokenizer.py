# Project 10: Compiler Part 1
#
# Yves Yang
#
# Tokenizer for jack code syntax analysis
import re


class Tokenizer:

    keyword = ["class", "constructor", "function", "method", "field", "static",
               "var", "int", "char", "boolean", "void", "true", "false",
               "null", "this", "let", "do", "if", "else", "while", "return"]
    symbol = ["{", "}", "(", ")", "[", "]", ",", ".", ";", "+", "-", "*", "/",
              "&", "|", "<", ">", "=", "~"]
    special_symbol = {"<": "&lt;", ">": "&gt;", "&": "&amp;", '"': "&quot;"}

    def __init__(self, codes):
        self.codes = codes
        self.tokens = self.get_tokens(codes)

    def get_tokens(self, codes):
        '''Take in jack codes and return tokens in a list'''
        result = ["<tokens>"]
        for line in codes:
            items = re.findall(r'[\w]+|"[^"\n]+"|[^\w ]', line)
            for i in items:
                if re.match(r'[0-9]', i[0]):
                    # Start with digit, must be an integerConstant.
                    result.append(f"<integerConstant> {i} </integerConstant>")
                elif i[0] == '"' and i[-1] == '"':
                    # Start and end with double quote, must be stringConstant.
                    result.append(f"<stringConstant> {i[1:-1]} </stringConstant>")
                elif i in self.keyword:
                    # Token is a keyword.
                    result.append(f"<keyword> {i} </keyword>")
                elif i in self.symbol:
                    if i in self.special_symbol:
                        i = self.special_symbol[i]
                    # Token is a symbol.
                    result.append(f"<symbol> {i} </symbol>")
                else:
                    # Token is an identifier.
                    result.append(f"<identifier> {i} </identifier>")
        result.append("</tokens>")
        return result
