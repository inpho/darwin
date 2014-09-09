#!bin/env ruby
#encoding: utf-8

import rython

ctx = rython.RubyContext(requires=["rubygems", "anystyle/parser"])
parser = ctx("Anystyle.parser")

mystring  = """Abbot, Francis Ellingwood. 1872. Truths for the times. Ramsgate,
Kent Thomas Scott."""

parser.parse(mystring)


