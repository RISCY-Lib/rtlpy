##########################################################################
# Python library to help with the automatic creation of RTL              #
# Copyright (C) 2022, Benjamin Davis                                     #
#                                                                        #
# This program is free software: you can redistribute it and/or modify   #
# it under the terms of the GNU General Public License as published by   #
# the Free Software Foundation, either version 3 of the License, or      #
# (at your option) any later version.                                    #
#                                                                        #
# This program is distributed in the hope that it will be useful,        #
# but WITHOUT ANY WARRANTY; without even the implied warranty of         #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
# GNU General Public License for more details.                           #
#                                                                        #
# You should have received a copy of the GNU General Public License      #
# along with this program.  If not, see <https://www.gnu.org/licenses/>. #
##########################################################################

from typing import Iterator, Optional, Tuple

from rtlpy.ply import lex

from rtlpy.parser.ast import Module
from rtlpy.parser.exceptions import UnbuiltLexerException


class VerilogLexer:
  """Verilog Lexical Analyzer"""

  mod = Module()

  def __init__(self):
    """Create a VerilogLexer"""
    self.lexer: Optional[lex.Lexer] = None

  def load_from_file(self, filename: str) -> None:
    """Opens the underlying file to lex

    Raises:
        UnbuiltLexerException: If the instances build method has not been called before this method

    Args:
        filename (str, optional): _description_. Defaults to None.
    """
    data = ""
    with open(filename, 'r') as f:
      for line in f.readlines():
        data += line

    if self.lexer is None:
      raise UnbuiltLexerException(f"Trying to load {type(self).__name__} from string w/o building")
    self.lexer.input(data)

  def load_from_string(self, data: str) -> None:
    """Loads the lexer from a data string

    Raises:
        UnbuiltLexerException: If the instances build method has not been called before this method

    Args:
        data (str): _description_
    """
    if self.lexer is None:
      raise UnbuiltLexerException(f"Trying to load {type(self).__name__} from string w/o building")
    self.lexer.input(data)

  def build(self, **kwargs):
    """Builds the Lexer
    """
    self.lexer = lex.lex(object=self, **kwargs)

  def token(self) -> lex.LexToken:
    """Get the next token from the lexer

    Raises:
        UnbuiltLexerException: If the instances build method has not been called before this method

    Returns:
        lex.LexToken: The next LexToken from the data input
    """
    if self.lexer is None:
        raise UnbuiltLexerException(f"Trying to tokenize using {type(self).__name__} w/o building")
    return self.lexer.token()

  def reset_lineno(self):
    if self.lexer is None:
      raise UnbuiltLexerException(f"Trying to reset lineno of {type(self).__name__} w/o building")

  def __iter__(self) -> Iterator[lex.LexToken]:
    while True:
      if self.lexer is None:
        raise UnbuiltLexerException(f"Trying to tokenize using {type(self).__name__} w/o building")
      tok = self.lexer.token()
      if not tok:
        break
      yield tok

  ##########################################################################
  # Tokens
  ##########################################################################

  reserved_keywords: Tuple[str, ...] = (
    "always", "and", "assign", "automatic", "begin", "buf",
    "bufif0", "bufif1", "case", "casex", "casez", "cell",
    "cmos", "config", "deassign", "default", "defparam", "design",
    "disable", "edge", "else", "end", "endcase", "endconfig",
    "endfunction", "endgenerate", "endmodule", "endprimitive", "endspecify", "endtable",
    "endtask", "event", "for", "force", "forever", "fork",
    "function", "generate", "genvar", "highz0", "highz1", "if",
    "ifnone", "initial", "instance", "inout", "input", "integer",
    "join", "large", "liblist", "localparam", "macromodule", "medium",
    "module", "nand", "negedge", "nmos", "nor", "not",
    "noshowcancelled", "notif0", "notif1", "or", "output", "parameter",
    "pmos", "posedge", "primitive", "pull0", "pull1", "pulldown",
    "pullup", "pulsestyle_onevent", "pulsestyle_ondetect", "rcmos", "real", "realtime",
    "reg", "release", "repeat", "rnmos", "rpmos", "rtran",
    "rtranif0", "rtranif1", "scalared", "signed", "showcancelled", "small",
    "specify", "specparam", "strength", "strong0", "strong1", "supply0",
    "supply1", "table", "task", "time", "tran", "tranif0",
    "tranif1", "tri", "tri0", "tri1", "triand", "trior",
    "trireg", "unsigned", "use", "vectored", "wait", "wand",
    "weak0", "weak1", "while", "wire", "wor", "xnor",
    "xor"
  )

  operators = (
    "INV", "AND", "OR", "XOR", "XNOR",
    "LSHIFT", "RSHIFT", "NAND", "NOR",
    "NOT", "AND_LOGICAL", "OR_LOGICAL",
    "EQ", "NEQ", "LT", "GT", "LTEQ",
    "GTEQ", "IDENTICAL", "NIDENTICAL",
    "CONDITIONAL", "RIGHTARROW",
    "PLUS", "MINUS", "MULTIPLY",
    "DIVIDE", "MODULO", "POWER",
    "ARITH_LSHIFT", "ARITH_RSHIFT"
  )

  literal_values = (
    "real",
    "unsigned_binary",
    "unsigned_octal",
    "unsigned_decimal",
    "unsigned_hexadecimal",
    "signed_binary",
    "signed_octal",
    "signed_decimal",
    "signed_hexadecimal",
    "string"
  )

  controls = (
    "AT", "COMMA", "COLON", "SEMICOLON", "DOT",
    "PLUSCOLON", "MINUSCOLON", "DELAY",
    "LPAREN", "RPAREN", "LBRACKET", "RBRACKET",
    "LBRACE", "RBRACE", "DOLLAR"
  )

  tokens = [key.upper() for key in reserved_keywords] + \
           [f"{op.upper()}_OPERATOR" for op in operators] + \
           [f"{lit.upper()}_LITERAL" for lit in literal_values] + \
           [c.upper() for c in controls] + \
           ['ID']

  skipped = ('BLOCKCOMMENT', 'LINECOMMENT', "DIRECTIVE")

  ##########################################################################
  # Skipped and ignored token definitions
  ##########################################################################

  t_ignore = ' \t\r'

  # Directives
  directive = r'''\`.*?\n'''

  @lex.TOKEN(directive)
  def t_DIRECTIVE(self, t: lex.LexToken):
    t.lexer.lineno += t.value.count("\n")
    pass

  # Comments
  linecomment = r'''//.*?\n'''
  blockcomment = r'''/\*(.|\n)*?\*/'''

  @lex.TOKEN(linecomment)
  def t_LINECOMMENT(self, t: lex.LexToken):
    t.lexer.lineno += t.value.count("\n")
    pass

  @lex.TOKEN(blockcomment)
  def t_BLOCKCOMMENT(self, t: lex.LexToken):
    t.lexer.lineno += t.value.count("\n")
    pass

  ##########################################################################
  # Operator Tokens
  ##########################################################################

  t_AND_LOGICAL_OPERATOR = r'&&'
  t_OR_LOGICAL_OPERATOR = r'\|\|'
  t_ARITH_LSHIFT_OPERATOR = r'<<<'
  t_ARITH_RSHIFT_OPERATOR = r'>>>'
  t_INV_OPERATOR = r'~'
  t_AND_OPERATOR = r'&'
  t_OR_OPERATOR = r'\|'
  t_XOR_OPERATOR = r'\^'
  t_XNOR_OPERATOR = r'~^|^~'
  t_LSHIFT_OPERATOR = r'<<'
  t_RSHIFT_OPERATOR = r'>>'
  t_NAND_OPERATOR = r'~&'
  t_NOR_OPERATOR = r'~\|'
  t_NOT_OPERATOR = r'!'
  t_EQ_OPERATOR = r'=='
  t_NEQ_OPERATOR = r'!='
  t_LT_OPERATOR = r'<'
  t_GT_OPERATOR = r'>'
  t_LTEQ_OPERATOR = r'<='
  t_GTEQ_OPERATOR = r'>='
  t_IDENTICAL_OPERATOR = r'==='
  t_NIDENTICAL_OPERATOR = r'!==='
  t_CONDITIONAL_OPERATOR = r'\?'
  t_RIGHTARROW_OPERATOR = r'->'
  t_PLUS_OPERATOR = r'\+'
  t_MINUS_OPERATOR = r'-'
  t_MULTIPLY_OPERATOR = r'\*'
  t_DIVIDE_OPERATOR = r'\/'
  t_MODULO_OPERATOR = r'%'
  t_POWER_OPERATOR = r'\*\*'

  ##########################################################################
  # Literal Values Tokens
  ##########################################################################

  # TODO: all tokens in literal_values
  real_pat = r"(([0-9]+[\.0-9]*)[eE][-]*[0-9]+)|([0-9]+\.[0-9]+)"
  unsigned_binary_pat = r'[0-9]*\'[bB][01_xXzZ]+'
  unsigned_octal_pat = r'[0-9]*\'[oO][0-7_xXzZ]+'
  unsigned_decimal_pat = r'([0-9]*\'[dD][0-9_]+)|([0-9]+)'
  unsigned_hexadecimal_pat = r'[0-9]*\'[hH][0-9a-fA-F_xXzZ]+'
  signed_binary_pat = r'[0-9]*\'[sS][bB][01_xXzZ]+'
  signed_octal_pat = r'[0-9]*\'[sS][oO][0-7_xXzZ]+'
  signed_decimal_pat = r'[0-9]*\'[sS][dD][0-9_]+'
  signed_hexadecimal_pat = r'[0-9]*\'[sS][hH][0-9a-fA-F_xXzZ]+'

  string_pat = r'"[\S]+"'

  @lex.TOKEN(real_pat)
  def t_REAL_LITERAL(self, t: lex.LexToken) -> lex.LexToken:
    return t

  @lex.TOKEN(unsigned_binary_pat)
  def t_UNSIGNED_BINARY_LITERAL(self, t: lex.LexToken) -> lex.LexToken:
    return t

  @lex.TOKEN(unsigned_octal_pat)
  def t_UNSIGNED_OCTAL_LITERAL(self, t: lex.LexToken) -> lex.LexToken:
    return t

  @lex.TOKEN(unsigned_hexadecimal_pat)
  def t_UNSIGNED_HEXADECIMAL_LITERAL(self, t: lex.LexToken) -> lex.LexToken:
    return t

  @lex.TOKEN(signed_binary_pat)
  def t_SIGNED_BINARY_LITERAL(self, t: lex.LexToken) -> lex.LexToken:
    return t

  @lex.TOKEN(signed_octal_pat)
  def t_SIGNED_OCTAL_LITERAL(self, t: lex.LexToken) -> lex.LexToken:
    return t

  @lex.TOKEN(signed_decimal_pat)
  def t_SIGNED_DECIMAL_LITERAL(self, t: lex.LexToken) -> lex.LexToken:
    return t

  @lex.TOKEN(signed_hexadecimal_pat)
  def t_SIGNED_HEXADECIMAL_LITERAL(self, t: lex.LexToken) -> lex.LexToken:
    return t

  @lex.TOKEN(string_pat)
  def t_STRING_LITERAL(self, t: lex.LexToken) -> lex.LexToken:
    return t

  @lex.TOKEN(unsigned_decimal_pat)
  def t_UNSIGNED_DECIMAL_LITERAL(self, t: lex.LexToken) -> lex.LexToken:
    return t

  ##########################################################################
  # Control Tokens
  ##########################################################################

  t_AT = r'@'
  t_COMMA = r','
  t_COLON = r':'
  t_SEMICOLON = r';'
  t_DOT = r'\.'
  t_PLUSCOLON = r'\+:'
  t_MINUSCOLON = r'-:'
  t_DELAY = r'\#'
  t_LPAREN = r'\('
  t_RPAREN = r'\)'
  t_LBRACKET = r'\['
  t_RBRACKET = r'\]'
  t_LBRACE = r'\{'
  t_RBRACE = r'\}'
  t_DOLLAR = r'\$'

  ##########################################################################
  # ID and key-word Tokens
  ##########################################################################

  identifier = r'''([a-zA-Z_])([a-zA-Z_0-9])*'''

  @lex.TOKEN(identifier)
  def t_ID(self, t: lex.LexToken):
    if (t.value in self.reserved_keywords):
      t.type = t.value.upper()
    else:
      t.type = 'ID'
    return t

  ##########################################################################
  # Misc Lexer Tokens
  ##########################################################################

  # Define a rule so we can track line numbers
  def t_newline(self, t):
    r'\n+'
    t.lexer.lineno += len(t.value)
