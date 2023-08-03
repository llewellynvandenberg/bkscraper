import requests
from utils import utils
from modules import modules
from scrape_rooms import scrape_rooms
import concurrent.futures
from datetime import datetime
import asyncio
import aiohttp
import json
import time


HEADERS = {
    "authority": "www.lekkeslaap.co.za",
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
    "content-type": "application/x-www-form-urlencoded",
    "origin": "https://www.lekkeslaap.co.za",
    "sec-ch-ua": "'Google Chrome';v='113', 'Chromium';v='113', 'Not-A.Brand';v='24'",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "'macOS'",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
}

URL = "https://www.lekkeslaap.co.za/forms/new_enquiry_form/backend/prices.php"

SITE = 'Lekke Slaap'


# async functions

async def fetch(s, url):
    try:
        async with s.request("POST", URL, data=url, headers=HEADERS) as r:
        
            if r.status != 200:
                r.raise_for_status()
            
            return await r.text()
    except:
        time.sleep(5)
        print('failure to retrieve data')
        return ''

async def fetch_all(s, urls):
    tasks = []

    count = 0
    for url in urls:
        task = asyncio.create_task(fetch(s, url))
        
        tasks.append(task)
        count +=1

    res = await asyncio.gather(*tasks)
    return res

async def main(urls):
    async with aiohttp.ClientSession(trust_env=True) as session:
        htmls = await fetch_all(session, urls)
        return htmls



def getResponse(url):
    response = requests.request("POST", URL, data=url, headers=HEADERS)
    return response


def scrape_variants(metadata):

    property_data = []
    df = metadata
    
    for p in range(3):#len(df['Property Code'])): # set up to 3 peroperties for testing
        # loop through properties (sync)
        prop_code = str(df.loc[p ,'Property Code']).replace('.0', '')
        
        room_info = scrape_rooms(prop_code)
        room_names = room_info['room_names']
        room_codes = room_info['room_codes']

        property = modules.Property(prop_code, p, room_codes)

        
        print(property.room_codes)


        for rc in range(len(room_codes)):
            room = modules.Room(room_codes[rc], room_names[rc])

            check_in = '2023-08-01'
            check_out = '2023-08-02'

            # construct payload
        
            adults = 1
            print(f'Current Room: {room_codes[rc]}')
            now = datetime.now()

            current_time = now.strftime("%H:%M:%S")
            print("Scraping room contents: ", current_time)

            payloads = []
            dates = []
            while str(check_in) != '2023-10-01':

                payload = f"establishment_id={prop_code}&start_date={utils.formatDate(check_in)}&end_date={utils.formatDate(check_out)}&allocation_details%5B{room_codes[rc]}%5D%5B1%5D%5Badults%5D={adults}&allocation_details%5B{room_codes[rc]}%5D%5Brooms%5D=1"
                payloads.append(payload)
                dates.append(check_in)

                check_in, check_out = utils.nextDay(check_in, check_out)

           

            responses = asyncio.run(main(payloads))
            #responses = []
            for r in range(len(responses)):

                response = responses[r]
                if response == '':
                    continue
                check_in = dates[r]
        
                    
            

                response = json.loads(response)

                available = 1
                if response['data']['prices']['provider'] != 'nightsbridge':
                    available = 0
                

                price = response['data']['prices']['basic_price']
        
                variant = modules.RoomVariant(check_in, price, available)
                
                room.variants.append(variant)
                
                
             

            property.rooms.append(room)

        
        property_data.append(property)

        

    return property_data

     
