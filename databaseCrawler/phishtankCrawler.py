import requests
from bs4 import BeautifulSoup
import csv
import time


baseURL = "https://phishtank.org/phish_archive.php?page="
pagesToScan  = 5
databaseResultsKnown = []
databaseResultsAll = []

for x in range (0, pagesToScan):
    currentPageScan = baseURL + str(x)
    
    # Requested HTML PAGE
    currentPageScan = requests.get(currentPageScan)

    #Beautiful soup create object and select the table from Phistank
    currentPageParsed = BeautifulSoup(currentPageScan.content, "html.parser")
    currentPageParsed = currentPageParsed.find("table", attrs={'class':'data'})

    currentPageResults = currentPageParsed.find_all('tr', style="background: #ffffcc;")

    for currentRow in currentPageResults:
        column = currentRow.find_all('td')
        column = [ele.text.strip(" ") for ele in column]
        del column[2]
        del column[0]
        column[0] = column[0].split("added",1)[0]
        databaseResultsKnown.append(column)

    rowDetails = ["SITE", "VALID?", "STATUS"]
    with open ("databaseResults.csv", "w+") as currentFile:
        write = csv.writer(currentFile)
        write.writerows(databaseResultsKnown)
        currentFile.close()
    
    time.sleep(5)
