import requests
from utils import utils
from modules import modules
import numpy as np
import asyncio
import aiohttp
import json
import time
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials

api_file_path = '/Users/llewellynvandenberg/Library/CloudStorage/OneDrive-Personal/Industry Above/phase1/lodge_dashboard/firebase/api_key/propertydashboard-b02fb-firebase-adminsdk-ig2rx-0930f6b367.json'

cred = credentials.Certificate(api_file_path)
firebase_admin.initialize_app(cred)
db = firestore.client()
ls_prop_dta = db.collection('kruger_ls')


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


async def get_data(session, url):
    async with session.request("POST", URL, data='', headers=HEADERS, params=url) as resp:
        response = await resp.text()
        return response


async def main(urls):
    _responses = []

    async with aiohttp.ClientSession(trust_env = True) as session:

        tasks = []
        for url in urls:
            tasks.append(asyncio.ensure_future(get_data(session, url)))

        tsks = await asyncio.gather(*tasks)
        for t in tsks:
            _responses.append(t)
    return _responses


def scrape(metadata, stop = 150):

    df = metadata
    
    for p in range(len(df['property_code'])):
        print(p)
        print(len(df['property_code']))
        # loop through properties (sync)
        prop_code = str(df.loc[p ,'property_code']).replace('.0', '')
        prop_name = str(df.loc[p ,'property_name'])
        prop_rating = str(df.loc[p ,'property_rating' ])

        print(prop_name)


        adults = 1
        max_people = 2
        responses = []
        min_nights = 0
        check_in = '2023-09-01'
        check_out = '2023-09-02'
        
        while 1:
            # initial request to see min nights stays
            querystring = {"start_date":utils.formatDateQ(check_in),"end_date":utils.formatDateQ(check_out),"pax":adults,"id":f"{prop_code}"}
            resp = requests.request("POST", URL, data='', headers=HEADERS, params=querystring)
            resp = json.loads(resp.text)
            try:
                min_nights = resp['units'][0]['min_stay']
                break
            except Exception as e:
                check_in, check_out = utils.nextDay(check_in, check_out)
                print(check_in)
                print(check_out)
                print(e)
              
        
                
        while 1:
            
            
            check_in = '2023-08-01'
            check_out = '2023-08-02'
            if min_nights>1:
                check_out = utils.getCheckOutDate(check_in, min_nights)


            if adults > max_people:
                break
            payloads = []
            dates = []

            while str(check_in) != '2023-11-01':

                querystring = {"start_date":utils.formatDateQ(check_in),"end_date":utils.formatDateQ(check_out),"pax":adults,"id":f"{prop_code}"}
                payloads.append(querystring)
                dates.append(check_in)

                check_in, check_out = utils.nextDay(check_in, check_out)

            # 1 adult info = responses[0]
            # 2 adult info = responses[1]

            while 1:
                try:
                    responses.append(asyncio.run(main(payloads)))
                    break
                except:
                    print('probably too many flippen files, lets try again')
                    time.sleep(10)
                    continue
            adults +=1

        responses = np.array(responses)
        

        responses_1 = responses[0]
        responses_2 = responses[1]
        print(time.perf_counter())

        _property = modules.Property(
            prop_code = prop_code, 
            prop_ID = p,
            prop_name = prop_name,
            prop_rating = prop_rating
            )

        # might need to use different index incase query failure

        
        for r in range(len(responses_1)):
            
            response = responses_1[r]
            response2 = responses_2[r]

            if response == '':
                continue
            check_in = dates[r]

            try:
                response = json.loads(response)
                response2 = json.loads(response2)
            except:
                print('could not load json')
                #print(response)
                continue

            try:
                response = response['units']
                response2 = response2['units']
            except:
                pass
            
            for room_index in range(len(response)):

                room = response[room_index]

                i2 = room_index
                init = 1
                while 1:
                    try:
                        if response[room_index]['id'] == response2[i2]['id']:
                            price_for_2 = response2[i2]['price']['from']['final_price']
                            break
                        if init:
                            i2=0
                            init = 0
                        else:
                            i2+=1
                    except:
                        price_for_2 = ''
                        break

                try:
                    if(int(room['price']['for']) > max_people):
                        max_people = int(room['price']['for'])

                    room_code = room['id']

                    
                    
                    if r == 0:
                    
                        _room = modules.Room(
                            room_code = room['id'],
                            room_name = room['name'],
                            beds = room['bed'],
                            occupency = room['sleeps']['adults'],
                            child_pol = room['minimum_child_age'],
                            cancel_pol = utils.getCancelDiff(check_in ,room['free_cancellation_promotion']['deadline']),
                            min_nights = room['min_stay']
                            )
                        _property.rooms.append(_room)
                        

                    _variant = modules.RoomVariant(
                        date = check_in,
                        price = room['price']['from']['final_price'],
                        price_2 = price_for_2,
                        availability = room['num_avail'],
                        party_size = room['price']['for'],
                        nights = min_nights
                    )
                except Exception as e:
                    print('could not add variants')
                    print(e)

                    _variant = modules.RoomVariant(
                        date = check_in,
                        price = '',
                        price_2 = '',
                        availability = 0,
                        party_size = '',
                        nights = min_nights
                    )

                    
                try:
                
                    if r!=0:
                        for ri in range(len(response)):

                            if _property.rooms[ri].room_code == room_code:
                                _property.rooms[ri].variants.append(_variant)
                    else:
                        _property.rooms[room_index].variants.append(_variant)
                except Exception as e:
                    print(e)


        ls_prop_dta.add(_property.to_dict())
    print(f'Successfully scraped and uplaoded {len(df["property_code"])} properties')
                
  
