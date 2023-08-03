import requests
from utils import utils
from modules import modules
import asyncio
import aiohttp
import json
import time
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials

api_file_path = '/Users/llewellynvandenberg/Library/CloudStorage/OneDrive-Personal/Industry Above/phase1/lodge_dashboard/firebase/api_key/propertydashboard-b02fb-firebase-adminsdk-ig2rx-0930f6b367.json'






URL = "https://www.lekkeslaap.co.za/forms/new_enquiry_form/backend/details.php"


PAYLOAD = ""
HEADERS = {
    "authority": "www.lekkeslaap.co.za",
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
    "referer": "https://www.lekkeslaap.co.za/accommodation/antrim-collection/book",
    "sec-ch-ua": '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}



SITE = 'Lekke Slaap'


# async functions

async def fetch(s, url):
    max_count = 10
    count = 0
    while 1:
        if count  == max_count:
            return ''
        count +=1
        try:
            async with s.request("POST", URL, data='', headers=HEADERS, params=url) as r:
            
                if r.status != 200:
                    r.raise_for_status()
                
                return await r.text()
        except:
            time.sleep(30)
            print('failure to retrieve data')

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
    response = requests.request("POST", URL, data='', headers=HEADERS, params=url)
    return response


def scrape(metadata, stop = 150):

    df = metadata
    
    for p in range(len(df['property_code'])):
        # loop through properties (sync)
        prop_code = str(df.loc[p ,'property_code']).replace('.0', '')
        prop_name = str(df.loc[p ,'property_name'])

        
        check_in = '2023-08-01'
        check_out = '2023-08-02'
        adults = 1


        payloads = []
        dates = []
        print(time.perf_counter())
        print(prop_code)
        while str(check_in) != '2023-11-01':

            querystring = {"start_date":utils.formatDateQ(check_in),"end_date":utils.formatDateQ(check_out),"pax":adults,"id":f"{prop_code}"}
            payloads.append(querystring)
            dates.append(check_in)

            check_in, check_out = utils.nextDay(check_in, check_out)


        responses = asyncio.run(main(payloads))
        print(time.perf_counter())

        _property = modules.Property(
            prop_code = prop_code, 
            prop_ID = p,
            prop_name = prop_name
            )

        # might need to use different index incase query failure
        response = responses[0]
        response = json.loads(response)


            

        for r in range(len(responses)):
            response = responses[r]
            
            if response == '':
                continue
            check_in = dates[r]

            response = json.loads(response)
            for room_index in range(len(response)):
                room = response[room_index]
                try:
                    if r == 0:
                    
                        _room = modules.Room(
                            room_code = room['id'],
                            room_name = room['name'],
                            beds = room['bed'],
                            occupency = room['sleeps']['adults'],
                            child_pol = room['minimum_child_age'],
                            cancel_pol = room['free_cancellation_promotion']['deadline'],
                            min_nights = room['min_stay']
                            )
                        _property.rooms.append(_room)

                    _variant = modules.RoomVariant(
                        date = check_in,
                        price = room['price']['from']['final_price'],
                        availability = room['availability'],
                        party_size = room['price']['for']
                    )
                except:
                    print(room)

                _property.rooms[room_index].variants.append(_variant)

        with api_file_path as file:
            cred = credentials.Certificate(file)
            firebase_admin.initialize_app(cred)
            db = firestore.client()
            ls_prop_dta = db.collection('lekke_slaap2')

            ls_prop_dta.add(_property.to_dict())
    print(f'Successfully scraped and uplaoded {len(df["property_code"])} properties')
                
  
