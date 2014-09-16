'''Choose from darwinonline.txt, cambridge.txt, and beagle.txt'''

import rython

from codecs import open

ctx = rython.RubyContext(requires=["rubygems", "anystyle/parser"])
ctx("Encoding.default_internal = 'UTF-8'")
ctx("Encoding.default_external = 'UTF-8'")

parser = ctx("Anystyle.parser")

unable_to_parse = 0

with open('beagle.txt', 'r') as readfile,open('beagle_anystyle','w') as writefile: 
    for line in readfile:
        try:
            writefile.write(str(parser.parse(line)))
        except:
            writefile.write("UNABLE TO PARSE")
            print "unable to parse"
            unable_to_parse += 1
            pass
        writefile.write("\n")    
    writefile.write(str(unable_to_parse))

