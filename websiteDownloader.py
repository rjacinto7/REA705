import requests
import time
from urllib.parse import urlparse

a_file = open("site.txt")
directory = "pages\\"
counter  = 1
headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'
    }

lines = a_file.readlines()
for line in lines:
    print(line)
    response = requests.get(url=line, headers=headers, timeout=5)
    print(response)
    response.close()
    time.sleep(2)
    '''
    page_content = response.text
    domain = urlparse(line).netloc
    filetoWrite = str(counter)+ "_"+ domain+ ".txt"
    with open(directory + filetoWrite, 'w', encoding='utf8') as fp:
        fp.write(page_content)
    counter = counter + 1
    '''