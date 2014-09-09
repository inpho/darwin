import json
from time import sleep
from urllib2 import urlopen
from urllib import quote_plus
import os.path
import xml.etree.ElementTree as ET


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
    return data['response']['docs'][0]

def gather_titles():
    """Takes all the titles from the Darwin Library XML document and write them into a file
    entitled 'titles.txt'
    """
    tree = ET.parse('bhl_darwin_collection.xml')
    root = tree.getroot()

    #finds all the 'Title' tags and writes the 'FullTitle' child for each of
    #them on their own line into a file
    filename = 'titles.txt'
    target = open(filename,'wb')  

    for title in root.findall('.//Result/Title/'):
    	name = (title.find('FullTitle').text).encode("utf-8")
        target.write(name)
        target.write("\n")
    target.close()

def get_htrcid():
    """Opens the 'titles.txt' file and find the HTRC id for each of the titles"""
    exportfile = 'htrc_ids.txt'
    importfile = 'titles.txt' 
    
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
