import json
from time import sleep
from urllib2 import urlopen
from urllib import quote_plus

import xml.etree.ElementTree as ET


def search(title, sleep_time=1):
    """ Queries the HTRC Solr index with a title and returns the resulting metadata.
Documentation: http://www.hathitrust.org/htrc/solr-api
"""
    # TODO: Parameterize hostname
    
    solr ="http://chinkapin.pti.indiana.edu:9994/solr/meta/select/?q=title:%s" % quote_plus(title)
    solr += "&wt=json" ## retrieve JSON results
    print solr
    # TODO: exception handling
    data = json.load(urlopen(solr))
    if sleep:
        sleep(sleep_time) ## JUST TO MAKE SURE WE ARE THROTTLED
    return data['response']['docs'][0]

if __name__ == '__main__':
    title = "An account of the Arctic regions"
    xml_map = search(title)
    tree = ET.parse('bhl_darwin_collection.xml')
    root = tree.getroot()
 #   print root.find("TitleID")
    print root.tag
 
    print (root.find('.//Result/Title/FullTitle')).text
   #     print e.attrib
 #   root.xpath = [@TitleID]