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
    #print title
    #print title.encode('utf-8')
    solr ="http://chinkapin.pti.indiana.edu:9994/solr/meta/select/?q=title:%s" % quote_plus(title)
    solr += "&wt=json" ## retrieve JSON results
    #print solr
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

    tree = ET.parse('bhl_darwin_collection.xml')
    root = tree.getroot()
    #print root.tag
    #print myDict   

    #finds all the 'Title' tags and print the 'FullTitle' child for each of them
    filename = 'titles.txt'
    target = open(filename,'wb')  

    for title in root.findall('.//Result/Title/'):
    	name = (title.find('FullTitle').text).encode("utf-8")
        target.write(name)
        target.write("\n")
    target.close()

    # find the first 'FullTitle' tag and prints it 
    
    #u =  root.find('.//Result/Title/FullTitle')
    #return u.encode('utf-8')
    #return unicode(root.find('.//Result/Title/FullTitle'))

def get_htrcid():
    title = "The anatomy and philosophy of expression"
    myDict = search(title)
    #filename = 'htrc_ids.txt'
    importfile = 'titles.txt' 
    for line in open(importfile):
        #print line
        line = line.rstrip('\n')
        myDict = search(line)

        #print myDict.get('id')
        #target.write(str(myDict))
        if myDict:
            print myDict.get('id')
    


if __name__ == '__main__':
    gather_titles()
    get_htrcid()
