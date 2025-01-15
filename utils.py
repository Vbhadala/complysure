import requests
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime



def fetch_bse():

 # Define the URL
 url = "https://www.sebi.gov.in/sebiweb/ajax/home/getnewslistinfo.jsp"

 # Define the headers
 headers = {
     "Accept": "*/*",
     "Accept-Language": "en-GB,en-IN;q=0.9,en-US;q=0.8,en;q=0.7",
     "Connection": "keep-alive",
     "Content-Type": "application/x-www-form-urlencoded",
     "Cookie": "JSESSIONID=69BFA50E29A9ADDD1CF4314819392AE8; _ga=GA1.3.847353249.1736582447; _gid=GA1.3.1431324268.1736582447; _ga_9HZ5J5Q3K5=GS1.3.1736593729.2.1.1736594055.60.0.0",
     "DNT": "1",
     "Origin": "https://www.sebi.gov.in",
     "Referer": "https://www.sebi.gov.in/sebiweb/home/HomeAction.do?doListing=yes&sid=1&ssid=7&smid=0",
     "Sec-Fetch-Dest": "empty",
     "Sec-Fetch-Mode": "cors",
     "Sec-Fetch-Site": "same-origin",
     "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36",
     "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
     "sec-ch-ua-mobile": "?1",
     "sec-ch-ua-platform": '"Android"',
 }

 # Define the payload (form data)
 data = {
     "nextValue": "2",
     "next": "s",
     "search": "",
     "fromDate": "",
     "toDate": "",
     "fromYear": "",
     "toYear": "",
     "deptId": "14",
     "sid": "1",
     "ssid": "7",
     "smid": "0",
     "ssidhidden": "7",
     "intmid": "8",
     "sText": "Legal",
     "ssText": "Circulars",
     "smText": "",
     "doDirect": "-1",
 }

 # Send the POST request
 response = requests.post(url, headers=headers, data=data)

 # Parse HTML response
 soup = BeautifulSoup(response.text, "html.parser")

 # Locate the table
 table = soup.find("table")  # Adjust this to match the table's tag and class if needed

 data = []

 if table:
     rows = table.find_all("tr")
     for row in rows[1:]:
         columns = row.find_all("td")
         row_data = []
         for col in columns:
             # Extract text from the column
             cell_text = col.text.strip()

             # Check if there's a link (<a>) inside the column
             link = col.find("a")
             if link and link.get("href"):
                 href = link["href"]
                 row_data.append({"text": cell_text, "href": href})
             else:
                 row_data.append({"text": cell_text})

         data.append(row_data)
 else:
     print("No table found in the response.")

 final = []
 for item in data:
     date = item[0]['text']
     title = item[1]['text']
     link = item[1]['href']
     

     final.append({'date': date,'title':title,'link':link})

 return final





def fetch_nse():

    url = "https://www.nseindia.com/api/circulars?fromDate=01-01-2025&toDate=11-01-2025&dept=INSP"

    headers = {
        "accept": "*/*",
        "accept-language": "en-GB,en-IN;q=0.9,en-US;q=0.8,en;q=0.7",
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36",
        "referer": "https://www.nseindia.com/resources/exchange-communication-circulars",
        "dnt": "1",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": '"Android"',
    }

    # Session to maintain cookies and headers
    session = requests.Session()
    session.headers.update(headers)

    try:
        # Initial request to establish cookies (if needed)
        response = session.get("https://www.nseindia.com")
        response.raise_for_status()

        # Fetch the circulars
        response = session.get(url)
        response.raise_for_status()  # Raise error for HTTP status codes 4xx/5xx

        # Parse and print the data
        data = response.json()['data']

        final = []
        for item in data:
            date_str = item['cirDate']
            title = item['sub']
            link = item['circFilelink']

            # Parse the string into a datetime object
            date_obj = datetime.strptime(date_str, "%Y%m%d")

            # Format the datetime object into the desired format
            date = date_obj.strftime("%b %d, %Y")
   
            final.append({'date': date,'title':title,'link':link})
           
        return final

    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")