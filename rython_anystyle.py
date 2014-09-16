import rython

from codecs import open

ctx = rython.RubyContext(requires=["rubygems", "anystyle/parser"])
ctx("Encoding.default_internal = 'UTF-8'")
ctx("Encoding.default_external = 'UTF-8'")

parser = ctx("Anystyle.parser")

unable_to_parse = 0

readfile = open("darwinonline.txt", "r", errors="ignore")
for line in readfile:
    try:
        print parser.parse(line)
    except:
        print "UNABLE TO PARSE"
        unable_to_parse += 1
        pass

print unable_to_parse

