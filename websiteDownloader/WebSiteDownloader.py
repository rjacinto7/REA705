from urllib.parse import urlparse
from pathlib import Path
import urllib.request
import urllib.error
import urllib.parse
import time
import argparse
import sys
import os

#setup arg parser so user can pass arguments
parser = argparse.ArgumentParser(description='Web Page Downloader')
parser.add_argument('-f', type=str, action='append', help='Text file of websites', required=True)
parser.add_argument('-o', type=str, action='append', help='Output directory', required=True)
parser.add_argument('-l', type=str, action='append', help='Log File', required=True)
arguments = parser.parse_args()

try:
    webPageFile = open(arguments.f[0])
except FileNotFoundError:
    print("The text file of web pages you specified does not exist")
    exit(0)    
logFile = arguments.l[0]

# creates output directory if it doesn't exist
outputDirectory = Path(arguments.o[0])
if not outputDirectory.exists():
    outputDirectory.mkdir()

#set the header for HTTP request
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'}
counter = 1

#loop through every website in text file
lines = webPageFile.readlines()
for site in lines:
    print(site)
    request = urllib.request.Request(url=site, headers=headers)
    #try to open url to fetch webpage 
    try:
        html = urllib.request.urlopen(request).read()
        domain = urlparse(site).netloc
        #every website is saved to a seperate text file
        fileToWrite = str(outputDirectory) + "\\" + str(counter)+ "_"+ domain + ".txt"
        with open(fileToWrite, 'wb') as pf:
            pf.write(html)
        counter = counter + 1
    #catches various exceptions and logs them in log file (HTTP errors, URL errors)
    except urllib.error.HTTPError  as e:
        with open(logFile, 'a') as lf:
            tempString = str(e.code) + " " + site
            lf.write(tempString)
    except urllib.error.URLError as e:
        if hasattr(e, 'reason'):
            with open(logFile, 'a') as lf:
                tempString = str(e.reason) + " " + site
                lf.write(tempString)
        elif hasattr(e, 'code'):
            with open(logFile, 'a') as lf:
                tempString = str(e.code) + " " + site
                lf.write(tempString)
