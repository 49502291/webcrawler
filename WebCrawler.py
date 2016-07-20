#!/usr/bin/env python

"""
Anthor: Yichen Cai
Version: 0.0.1
Date: 2016-7-12
Language: python
Editor: sublime
"""

import urllib
import urlparse
from bs4 import BeautifulSoup
from sets import Set
import time
import threading
import Queue

#root url 
root = "http://www.google.com/"
#specialsign = "#"

# A synchronized queue class 
tovisit = Queue.Queue()
tovisit.put(root)

visited = Set()
# Set number of threads 
WORKER_THREAD_NUM = 4 
threadLock = threading.Lock()




class Crawler(threading.Thread):

    def __init__(self, id, timeout, threadLock):
        super(Crawler, self).__init__()
        self.thread_id = id
        self.timeout = timeout
        self.threadLock = threadLock

    def run(self):

        start  = time.time()
        end  =  start
        global tovisit
        global visited


        while True:

            if tovisit.empty() == False:

                start = time.time()
                url = tovisit.get()

                try:
                    response = urllib.urlopen(url)
                    content = response.read()
                except Exception as e:
                    print + " ***Failed***      "  + str(e)

                # Crawl page
                bs = BeautifulSoup(content, "html.parser")

                # Add new urls to queue 
                self.threadLock.acquire()
                print "***visiting***     "  + url
                addURLs(bs)
                self.threadLock.release()


            else:
                # if the queue keeping empty for more than certain threshhold, end this thread 
                end = time.time()
                if(end - start > self.timeout):
                    break



def addURLs(bs):


    """
    Get all internal links in current page, then append new links to queue 

    Args: 
        bs : Beautifulsoup instance represents current crawling object 
    Returns:

    """

    global tovisit
    global visited

    for tag in bs.findAll('a', href = True):

        newlink = tag['href']

        if(newlink.startswith("http")):
            if not newlink.startswith(root):
                continue
        else:
            newlink = urlparse.urljoin(root, tag['href'])


        if newlink[len(newlink)-1] == "/":
            newlink = newlink[:len(newlink) - 1]

        # check if this is an internal link and if it is alread visited     
        if newlink.startswith(root) and specialsign not in newlink and newlink not in visited:
            tovisit.put(newlink)
            visited.add(newlink)


def main() :

    global tovisit
    threads = []

    for i in range(WORKER_THREAD_NUM) :

        crawler = Crawler(i, 20, threadLock)
        threads.append(crawler)


    for t in threads:
        t.start()


    for t in threads:
        t.join()

    print "Tasks  Complete ........"



if __name__ == '__main__':
    main()









