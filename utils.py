import requests
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime


ra_ia_dept_id = 9
exchange_dept_id = 14

# Get current date
current_date = datetime.now()



from_date = '01-07-2024'
to_date = current_date.strftime('%d-%m-%Y') #'10-02-2025'

#date format for SEBI and NSE is DD-MM-YYYY

#fetch_sebi_exchange, fetch_nse_exchange, fetch_sebi_ra_ia, fetch_nse_ra_ia

# Keywords to filter out
keywords = ["Research Analysts", "Investment Advisers"]

def all_sebi():

    # Get current date
    current_date = datetime.now()

    from_date = '01-11-2024'
    to_date = current_date.strftime('%d-%m-%Y') #'10-02-2025'

    
    all_data = []
    
    for dept in [14, 15]:    
        data = fetch_sebi_exchange(from_date, to_date, dept)
        all_data.extend(data)
    
    all_dept = fetch_sebi_exchange(from_date, to_date, '-1')
    ex = ["SEBI Regulated Entities", "Stock Brokers", "Stock Exchange"]
    all_dept_final = [item for item in all_dept if any(kw.lower() in item.get('title', '').lower() for kw in ex)]

    all_data.extend(all_dept_final)

    # Removing duplicates based on 'title'
    unique_data = {item['title']: item for item in all_data}.values()

    # Convert back to a list if needed
    all_data = list(unique_data)# Removing duplicates based on 'title'

    # Sort all_data by the 'date' field (formatted as 'Feb 21, 2025')
    all_data.sort(key=lambda x: datetime.strptime(x['date'], "%b %d, %Y"), reverse=True)  # Sort in descending order

    return all_data

def all_mcx():
    
    all_data = []

    for month in ['03', '02', '01']:    
        data = fetch_mcx(month)
        all_data.extend(data)

    return all_data


def fetch_sebi_exchange(from_date, to_date, dept):

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
     "nextValue": "1",
     "next": "s",
     "search": "",
     "fromDate": from_date,
     "toDate": to_date,
     "fromYear": "",
     "toYear": "",
     "deptId": dept,
     "sid": "1",
     "ssid": "7",
     "smid": "0",
     "ssidhidden": "7",
     "intmid": "-1",
     "sText": "Legal",
     "ssText": "Circulars",
     "smText": "",
     "doDirect": "-1",
    }
    
    # print(data)
    
    # Send the POST request
    response = requests.post(url, headers=headers, data=data)
    
    # print(response)
    
    # Parse HTML response
    soup = BeautifulSoup(response.text, "html.parser")
    # print(soup)
    
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
    
    f_data = [item for item in final if not any(kw.lower() in item.get('title', '').lower() for kw in keywords)]
    
    return f_data
    
    

def fetch_sebi_ra_ia():

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
     "nextValue": "1",
     "next": "s",
     "search": "",
     "fromDate": from_date,
     "toDate": to_date,
     "fromYear": "",
     "toYear": "",
     "deptId": "14",
     "sid": "1",
     "ssid": "7",
     "smid": "0",
     "ssidhidden": "7",
     "intmid": "-1",
     "sText": "Legal",
     "ssText": "Circulars",
     "smText": "",
     "doDirect": "-1",
 }

 # print(data)

 # Send the POST request
 response = requests.post(url, headers=headers, data=data)

 # print(response)

 # Parse HTML response
 soup = BeautifulSoup(response.text, "html.parser")
 # print(soup)

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

 f_data = [item for item in final if any(kw.lower() in item.get('title', '').lower() for kw in keywords)]

 return f_data



def fetch_sebi_mf_pms():

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
     "nextValue": "1",
     "next": "s",
     "search": "",
     "fromDate": from_date,
     "toDate": to_date,
     "fromYear": "",
     "toYear": "",
     "deptId": "9",
     "sid": "1",
     "ssid": "7",
     "smid": "0",
     "ssidhidden": "7",
     "intmid": "-1",
     "sText": "Legal",
     "ssText": "Circulars",
     "smText": "",
     "doDirect": "-1",
 }

 # print(data)

 # Send the POST request
 response = requests.post(url, headers=headers, data=data)

 # print(response)

 # Parse HTML response
 soup = BeautifulSoup(response.text, "html.parser")
 # print(soup)

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

    from_date = '01-07-2024'
    to_date = current_date.strftime('%d-%m-%Y') #'10-02-2025'


    url = f"https://www.nseindia.com/api/circulars?fromDate={from_date}&toDate={to_date}&dept=INSP"

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

        # Remove entries where 'title' contains 'Surrender of Membership'
        filtered_data = [item for item in data if 'surrender of membership' not in item.get('sub', '').lower()]
        
        final = []
        for item in filtered_data:
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



def fetch_mcx(month='03'):
    
    url = "https://www.mcxindia.com/backpage.aspx/GetCircularSearch"

    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-GB,en-IN;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "DNT": "1",
        "Origin": "https://www.mcxindia.com",
        "Referer": "https://www.mcxindia.com/circulars/membership-compliance",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": '"Android"',
        "Cookie": "ASP.NET_SessionId=2lci35vwpip00uo3prz0rlus; _gid=GA1.2.574009522.1736766707; _gat_gtag_UA_121835541_1=1; _ga_8BQ43G0902=GS1.1.1736766706.1.0.1736766706.0.0.0; _ga=GA1.1.349469646.1736766707"
    }

    data = {
        "CircularType": "membership-and-compliance",
        "Year": "2025",
        "Month": month
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        data = result['d']
        final = []
        for item in data:
         date = item['DisplayCircularDate']
         title = item['Title']
         link = item['Documents']
         final.append({'date': date,'title':title,'link':link})


        # Remove entries where 'title' contains 'Surrender of Membership'
        filtered_data = [item for item in final if 'surrender of membership' not in item.get('title', '').lower()]
    
        return filtered_data

    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return {}



def fetch_cdsl():


    kw_exclude = ["DETAILS OF CHANGE OF RTA EFFECTED BY ISSUER", 
                "DETAILS OF SECURITIES ADMITTED WITH CDSL", 
                "WITHDRAWAL OF SECURITIES FROM CDSL", 
                "DETAILS OF CORPORATE ACTION"]
    
    url = "https://www.cdslindia.com/Publications/Communique.aspx"

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "en-GB,en-IN;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cache-Control": "max-age=0",
        "DNT": "1",
        "Priority": "u=0, i",
        "Sec-Ch-Ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        "Sec-Ch-Ua-Mobile": "?1",
        "Sec-Ch-Ua-Platform": '"Android"',
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36",
        "Cookie": "_gid=GA1.2.890368200.1736766904; _gat_gtag_UA_66604853_2=1; _ga_J0BFBWN0GT=GS1.1.1736766903.2.0.1736766903.0.0.0; _ga=GA1.1.1265784374.1734770367"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:

        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table")

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
             date = item[3]['text']
             title = item[2]['text']
             link = item[2]['href'][3:]
             final.append({'date': date,'title':title,'link': ('https://www.cdslindia.com/' + link)})

        f_data = [item for item in final if not any(kw.lower() in item.get('title', '').lower() for kw in kw_exclude)]
        
        return f_data


    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return {}




