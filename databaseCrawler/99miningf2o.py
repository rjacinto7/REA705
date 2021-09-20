import requests
from bs4 import BeautifulSoup
import csv


#yoho
base_url = "https://phishtank.org/phish_archive.php?page="
page_num  = 1

#Asks for how many pages to crawl
total_page_num = int(input("Please select how many pages you'd like to Crawl on PhishTank: "))
#Check if pages is greater than 0
if total_page_num <= 0:
    print("Invalid input. Pages should be greater than 0. Please try again... \n")
    exit()

#Two arrays. One for Valid and one for invalid phishing links
notscam = []
scam = []

for i in range (0, total_page_num, 1):
    # baseurl + page number
    full_url = base_url+str(i)
    
    # Requested HTML PAGE
    page = requests.get(full_url)

    #Beautiful soup create object and select the table from Phistank
    soup1 = BeautifulSoup(page.content, "html.parser")
    goodsoup = soup1.find("table", attrs={'class':'data'})

    # Defines two objects where rows is not valid and scam_rows is Valid Phish based off Phishtank's website.
    rows = goodsoup.find_all('tr', style="background: #ffffff;")
    scam_rows = goodsoup.find_all('tr', style="background: #ffffcc;")

    #Appends to the not_scam array containing the entries of the non-valid phishing entries in the table
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        notscam.append([ele for ele in cols if ele])
    #Appends to the scam array containing the entries of the valid phishing entries in the table
    for row in scam_rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        scam.append([ele for ele in cols if ele])
    
    #print(full_url)
    


#Writes the array to a CSV file
with open ("output_notscam.csv", "w+") as csv1:
        newarray = csv.writer(csv1,delimiter=',')
        newarray.writerows(notscam)
with open ("output_scam.csv", "w+") as csv2:
        newscamarray = csv.writer(csv2,delimiter=',')
        newscamarray.writerows(scam)

#print(scam)
#print(goodsoup_body)
#print(goodsoup)
