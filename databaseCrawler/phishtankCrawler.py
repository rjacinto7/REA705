import requests
from bs4 import BeautifulSoup
import csv
import time
import os
import sys
import urllib
from urllib.parse import urlparse
import re

os.chdir(os.path.dirname(os.path.abspath(__file__)))
baseURL = "https://phishtank.org/phish_search.php?page="
endURL = "&valid=n&Search=Search"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'}
pagesToScan  = 100
#This is for checking if we already have the URL
allHTML = []
#This is for the websites we can access both URL and HTML
validURLHTML = [["site","form", "method=post", "method=get", "script", "javascripts", "iframe","applet", "frame", "type=submit", "email", "password", "button", "length", "At Sign", "Forward Slashes", "www Present", "periods", "dashes", "underscores", "number of digits", "has ASCII"]]
#This is for the websites we can only get the URL for
onlyURL = [["site","length", "At Sign", "Forward Slashes", "www Present", "periods", "dashes", "underscores", "number of digits", "has ASCII"]]

#Returns list of HTML features
def htmlCounter(htmlString):
    htmlCount = []
    htmlCount.append(htmlString.count('</form>'))
    htmlCount.append(htmlString.count('formmethod="post"'))
    htmlCount.append(htmlString.count('formmethod="get"'))
    htmlCount.append(htmlString.count('</script>'))
    htmlCount.append(htmlString.count('.js'))
    htmlCount.append(htmlString.count('</iframe>'))
    htmlCount.append(htmlString.count('</applet>'))
    htmlCount.append(htmlString.count('</frame>'))
    htmlCount.append(htmlString.count('type="submit'))
    htmlCount.append(htmlString.count('email'))
    htmlCount.append(htmlString.count('password'))
    htmlCount.append(htmlString.count('</button>'))
    return htmlCount

#Produces list of URL features
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
    return urlCount

def featureCount (site):
    featureCount = []
    #Site can be reached and HTML can be read
    try:
        #Try to reach the site
        site = str(site)
        request = urllib.request.Request(url=site, headers=headers)
        #normalize html code to search specific keywords
        pageHTML = str(urllib.request.urlopen(request).read())
        pageHTML = pageHTML.lower()
        return htmlCounter(pageHTML)
    #Sites that cant be reached
    except:
        return False

#takes the shortened URLs and gets the full one
def handleOddURL(badURL):
    investigateURL = "https://phishtank.org/phish_detail.php?phish_id=" + str(badURL)
    currentPageFullUrlScan = requests.get(investigateURL)
    if currentPageFullUrlScan.status_code == 200:
        detailedPageParsed = BeautifulSoup(currentPageFullUrlScan.content, "html.parser")
        detailedPageParsed = detailedPageParsed.find("div", {"id":"main"})
        detailedPageResults = detailedPageParsed.find_all('span', style="word-wrap:break-word;")
        for currentRow in detailedPageResults:
            detailedColumn = currentRow.find_all('b')
            detailedColumn = [ele.text.strip(" ") for ele in detailedColumn]
            return detailedColumn[0]
    else:
        return False

for x in range (51, pagesToScan):
    currentPageScan = baseURL + str(x) + endURL
    
    # Requested HTML PAGE
    currentPageScan = requests.get(currentPageScan)

    #Beautiful soup create object and select the table from Phistank
    currentPageParsed = BeautifulSoup(currentPageScan.content, "html.parser")
    currentPageParsed = currentPageParsed.find("table", attrs={'class':'data'})
    currentPageResults = currentPageParsed.find_all('tr', style="background: #ffffcc;")

    #Grab the URL 
    for currentRow in currentPageResults:
        #Grab all phishing URLS
        column = currentRow.find_all('td')
        column = [ele.text.strip(" ") for ele in column]
        #Parse the site in the column
        column[1] = column[1].split("added",1)[0]
        site = column[1]
        #Query for the site 
        if site[-3:] == "..." or "[email protected]" in site:
            site = handleOddURL(column[0])
        #If the site passes the conditions of being able to be retrieved, and not already scanned then
        if site != False:
            if site not in allHTML:
                final = []
                final.append(str(site))
                allHTML.append(str(site))
                x = featureCount(site)
                #If the site is not in the scanned URLs and we can retrieve URL + HTML add to validURLHTML
                if x != False:
                    final += x
                    final += urlFeatureCounter(site)
                    validURLHTML.append(final)
                #If the site is down just get the url features 
                else:
                    final += urlFeatureCounter(site)
                    onlyURL.append (final)
        print (final)
    time.sleep(5)

with open ("allFeatures2.csv", "w",  newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(validURLHTML)

with open ("urlFeaturesOnly2.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(onlyURL)