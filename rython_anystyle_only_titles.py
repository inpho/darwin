'''Takes a .txt file and passes it through AnySyle to create a new .txt file with the results.
Choose from cambridge.txt, cambridge.txt, and beagle.txt'''

'''
Naming conventions: 

For example, if the volume title was 'cambridge'.

INPUT:
cambridge.txt - text file with a listing of citations. This file must be created
    before you run the program and it's name must set as the volume_tile for the
    program to run

OUTPUT:
cambridge_titles.txt - text file with a listing of the titles that were extracted 
    from the citations with one title per line
cambridge_ids.txt - text file with a listing of all the found HTRC ids with an 
    id per line

'''



import json
from time import sleep
from urllib2 import urlopen
from urllib import quote_plus
import os.path

import rython

from codecs import open

ctx = rython.RubyContext(requires=["rubygems", "anystyle/parser"])
ctx("Encoding.default_internal = 'UTF-8'")
ctx("Encoding.default_external = 'UTF-8'")

parser = ctx("Anystyle.parser")

'set the title of the input volume you are working on'
volume_title = 'cambridge'


def gather_titles():
    unable_to_parse = 0

    with open(volume_title + '.txt', 'r') as readfile,open(volume_title + '_titles.txt','w') as writefile: 
        for line in readfile:
            try:
                dictionaryset = parser.parse(line)
                for dictionary in dictionaryset:
                    writefile.write(dictionary['title'])
                    writefile.write("\n")
            except:
                print "unable to parse"
                unable_to_parse += 1
                pass
         
def search(title, sleep_time=1):
    """ Queries the HTRC Solr index with a title and returns the resulting metadata.
    Documentation: http://www.hathitrust.org/htrc/solr-api
    """
    # TODO: Parameterize hostname	
    solr ="http://chinkapin.pti.indiana.edu:9994/solr/meta/select/?q=title:%s" % quote_plus(title)
    solr += "&wt=json" ## retrieve JSON results
    # TODO: exception handling
    try:
        data = json.load(urlopen(solr))
    except ValueError :
        print "No result found for " + title
        return
    if sleep:
        sleep(sleep_time) ## JUST TO MAKE SURE WE ARE THROTTLED
    try:
        return data['response']['docs'][0]
    except IndexError:
        return None

def get_htrcid():
    """Opens the 'titles.txt' file and find the HTRC id for each of the titles"""
    exportfile = volume_title + '_ids.txt'
    importfile = volume_title + '_titles.txt' 
    
    export = open(exportfile, 'wb')

    for line in open(importfile):
        #removes all of the extraneous characters in the title
        line = line.rstrip('\n')
        line = line.replace("/", "")
        line = line.replace(":", "")
        line = line.replace("[", "")
        line = line.replace("]", "")
        myDict = search(line)

        if myDict:
            export.write(myDict.get('id'))
            export.write('\n')
    export.close()

if __name__ == '__main__':
    gather_titles()
    get_htrcid()
