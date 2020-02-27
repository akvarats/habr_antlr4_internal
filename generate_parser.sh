#!/bin/bash

cd ./grammar
java -jar /usr/local/lib/antlr-4.8-complete.jar -o ../generated PlSqlLexer.g4 PlSqlParser.g4 -no-listener -visitor -Dlanguage=Python3