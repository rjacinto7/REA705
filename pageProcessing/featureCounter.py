from urllib.parse import urlparse
from pathlib import Path
import urllib.request
import urllib.error
import urllib.parse
import time
import argparse
import sys
import os
import csv

#set current running files path as current working directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

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

#loop through every website in text file
lines = webPageFile.readlines()
for site in lines:
    site = str(site)
    request = urllib.request.Request(url=site, headers=headers)

    #try to open url to fetch webpage 
    try:
        #normalize html code to search specific keywords
        pageHTML = str(urllib.request.urlopen(request).read())
        featureCount = []

        #Website URL 
        featureCount.append(urlparse(site).netloc)

        #Page features based off of Table 1 in proposal 
        featureCount.append(pageHTML.count('</form>'))
        featureCount.append(pageHTML.count('formmethod="post"'))
        featureCount.append(pageHTML.count('formmethod="get"'))
        featureCount.append(pageHTML.count('</script>'))
        featureCount.append(pageHTML.count('.js'))
        featureCount.append(pageHTML.count('</iframe>'))
        featureCount.append(pageHTML.count('</applet>'))
        featureCount.append(pageHTML.count('</frame>'))
        featureCount.append(pageHTML.count('type="submit'))
        featureCount.append(pageHTML.count('input email'))
        featureCount.append(pageHTML.count('password'))
        featureCount.append(pageHTML.count('</button>'))

        #every website is saved to a seperate text file
        fileToWrite = str(outputDirectory) + ".csv"
        with open(fileToWrite, "a") as pf:
            write = csv.writer(pf)
            write.writerow(featureCount)


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
