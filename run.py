import os
import sys
#sys.path.append(os.path.join(os.path.dirname(__file__), "generated"))

from antlr4 import *
from parser.PlSqlLexer import PlSqlLexer
from parser.PlSqlParser import PlSqlParser
from parser.CaseChangingStream import CaseChangingStream
from translator import Translator


if __name__ == "__main__":

    if len(sys.argv) > 1:
        with open(sys.argv[1], "rt") as f:
            content = f.read()
    else:
        content = sys.stdin.read()

    lexer = PlSqlLexer(CaseChangingStream(InputStream(content), True))
    stream = CommonTokenStream(lexer)

    parser = PlSqlParser(stream)
    translator = Translator()

    ora_root = parser.sql_script()
    pg_root = translator.translate(ora_root)

    print("PG root: {}".format(pg_root))

