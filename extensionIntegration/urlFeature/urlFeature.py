#Original code from websiteDownloader
from urllib.parse import urlparse
from pathlib import Path
import urllib.request
import urllib.error
import urllib.parse
import argparse
import sys
import os
import re

#set current running files path as current working directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

#set the header for HTTP request
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'}


#Take a site URL and count its  URL Features
def urlFeatureCounter(site):
    hostname = urlparse(site).netloc
    site = str(site)
    urlCount = []
    urlCount.append(len(site))
    urlCount.append(site.count("@"))
    urlCount.append(site.count("/"))
    #Checks for presence of "www" in url | 1 = TRUE, 0 = FALSE
    if "www" in site:
        urlCount.append(site.count("1"))
    else:
        urlCount.append(site.count("0"))
    #Hostname Counts
    urlCount.append(hostname.count("."))
    urlCount.append(hostname.count("-"))
    urlCount.append(hostname.count("_"))
    #Counts the number of digits in hostname
    digits = 0
    for character in hostname:
        if character.isdigit():
            digits += 1
    urlCount.append(digits)
    #Checks if the URL is all ascii characters 
    onlyAscii = lambda s: re.match('^[\x00-\x7F]+$', s) != None
    if onlyAscii == True:
        urlCount.append(site.count("1"))
    else:
        urlCount.append(site.count("0"))

    totalCount = ' '.join(str(e) for e in urlCount)
    return totalCount


#Take a site URL and count its Page Features
def pageFeatureCounter(site):
    #try to open url to fetch webpage 
    try:
        site = str(site)
        request = urllib.request.Request(url=site, headers=headers)
        #normalize html code to search specific keywords
        pageHTML = str(urllib.request.urlopen(request).read())
        featureCount = []

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
        totalCount = ' '.join(str(e) for e in featureCount)
        return totalCount

    #catches various exceptions and logs them in log file (HTTP errors, URL errors)
    except urllib.error.HTTPError  as e:
        return "Error reaching site."
    except urllib.error.URLError as e:
        return "Error reaching site."
        

