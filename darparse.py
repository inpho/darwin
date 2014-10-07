'''
Takes a plaintext file of unparsed bibliography entries and parses them using
AnyStyle.io. Then performs a search for the title on the HathiTrust and returns
matching IDs. The final data is output as a JSON struct for use on the web,
particularly with the corpus builder tool at
http://github.com/inpho/corpus-builder

Run with 'python darparse.py -h' to see a list of command arguments.
'''
import json
from time import sleep
from urllib2 import urlopen
from urllib import quote_plus
import os.path
import xmlrpclib

import rython

from codecs import open

ctx = rython.RubyContext(requires=["rubygems", "anystyle/parser"])
ctx("Encoding.default_internal = 'UTF-8'")
ctx("Encoding.default_external = 'UTF-8'")

anystyle = ctx("Anystyle.parser")

'set the title of the input volume you are working on'
volume_title = 'cambridge'

def parse_citations_from_file(citation_file):
    return_list = []
    with open(citation_file, 'r') as readfile:
        for i, line in enumerate(readfile):
            line = line.decode('latin-1').encode("utf-8").strip()
            if line:
                try:
                    parsed = anystyle.parse(line)[0]
                    return_list.append({'original' : line, 'parsed' : parsed})
                except xmlrpclib.Fault:
                    return_list.append({'original' : line, 'parsed' : None})
                    print "error on line %d: %s" % (i, line)

    return return_list
         
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

def populate_htrc(citations):
    for citation in citations:
        citation['htrc_id'] = None
        citation['htrc_md'] = None
        if citation['parsed']:
            title = citation['parsed'].get('title')
            if title:
                title = title.replace("/", "")
                title = title.replace(":", "")
                title = title.replace("[", "")
                title = title.replace("]", "")
                htrc_md = search(title.encode('utf-8'))
            
                if htrc_md:
                    citation['htrc_md'] = htrc_md
                    citation['htrc_id'] = htrc_md.get('id')

    return citations

def extant_file(x):
    """
    'Type' for argparse - checks that file exists but does not open.
    """
    if not os.path.isfile(x):
        raise argparse.ArgumentError("%s does not exist" % x)
    return x

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-o', dest='output', help="output file", default='out.json')
    parser.add_argument('citation_file', help="citation file", 
        type=extant_file)
    args = parser.parse_args()

    citations = parse_citations_from_file(args.citation_file)
    citations = populate_htrc(citations)

    with open(args.output, 'wb') as output_file:
        json.dump(citations, output_file)

