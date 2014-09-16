import rython
ctx = rython.RubyContext(requires=["rubygems", "anystyle/parser"])
ctx("Encoding.default_internal = 'UTF-8'")
ctx("Encoding.default_external = 'UTF-8'")

parser = ctx("Anystyle.parser")

mystring = """Abbot, Francis Ellingwood. 1872. Truths for the times. Ramsgate, Kent Thomas Scott."""

print type(mystring)
print parser.parse(mystring)
