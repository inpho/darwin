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
    solr ="http://chinkapin.pti.indiana.edu:9994/solr/meta/select/?q=title:%s" % quote_plus(title.encode("utf-8"))
    solr += "&wt=json" ## retrieve JSON results
    # print solr
    # TODO: exception handling
    data = json.load(urlopen(solr))
    if sleep:
        sleep(sleep_time) ## JUST TO MAKE SURE WE ARE THROTTLED
    return data['response']['docs'][0]

def gather_titles():

    tree = ET.parse('bhl_darwin_collection.xml')
    root = tree.getroot()
    print root.tag
  
    #finds all the 'Title' tags and print the 'FullTitle' child for each of them
    for title in root.findall('.//Result/Title/'):
       return unicode(title.find('FullTitle').text)
    
    # find the first 'FullTitle' tag and prints it 
    
    #u =  root.find('.//Result/Title/FullTitle')
    #return u.encode('utf-8')
    #return unicode(root.find('.//Result/Title/FullTitle'))

def get_htrcid(mytitle):
    title = "The anatomy and philosophy of expression"
    myDict = (gather_titles())
    #myDict = search(title)
    '''filename = 'test.xml'
    target = open(filename,'wb')
    target.write(str(myDict))
    print myDict
    '''
    print myDict.get('id')
    


if __name__ == '__main__':
    mytitle = "0"
    get_htrcid(mytitle)


