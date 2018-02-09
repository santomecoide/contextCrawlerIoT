#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Beacon import Beacon
from soapClient import SoapClient
from spider import Spider
import threading
import keyboard
import time
import os
import sys

context_thread = None

def contextualize(link):
    expanded_words = []

    clearscreen()
    print "\t\t################### --- start spider --- ###################"
    print "\n"
    print "\t\turl: " + str(link)
    soap = SoapClient()
    spider = Spider(url = link)

    object_name = spider.getObjectName()

    print "\t\t-----------------------------------------------------------"
    print "\t\tOject Name: " + str(object_name)
    print "\t\t-----------------------------------------------------------"

    for m_word in spider.getMetadataWords():
        print "\t\tAnalize Word: " + str(m_word)
        expanded_words = expanded_words + soap.getExpandedWords(m_word)

    print "\t\t-----------------------------------------------------------"
    print "\t\tExpanded Words:"
    for e_word in expanded_words:
        print "\t\t" + str(e_word)
    print "\t\t-----------------------------------------------------------"

    if len(expanded_words) > 0:
        print "\t\tStart Index Task"
        object_id = spider.getObjectId()
        soap.loadId(object_id)
        print "\t\t" + str(object_name) + "Is Now Indexed"
    else:
        print "\t\t" + str(object_name) + "Not Have Context Match"

    spider.stop()
    print "\n"
    print "\t\t################### --- end spider --- ###################"
    print "press 'c' to continue scan..."

def clearscreen():
	if(sys.platform == "linux" or sys.platform == "linux2"):
		os.system('clear')
	if(sys.platform == "win32"):
		os.system('cls')

def scan_beacon():
    print "scan beacons..."
    global context_thread

    beacon = Beacon()
    beacon.scanTask()
    if beacon.is_beacon_ready():
        context_thread = threading.Thread(target=contextualize, args=(beacon.get_url(), ))
        context_thread.start()
    else:
        scan_beacon()

if __name__ == '__main__':
    clearscreen()
    scan_beacon()
    while True:
        pass
        if keyboard.is_pressed('c'):
            if context_thread == None:
                clearscreen()
                scan_beacon()
            else:
                if context_thread.isAlive() == False:
                    clearscreen()
                    scan_beacon()
