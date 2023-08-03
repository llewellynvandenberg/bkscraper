import requests
import pandas as pd
import datetime
import re
import json
import pickle


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

### functions
        

### main
property_data = []
def main():
    df = pd.read_excel('data/lekkeslaap_metadata_stellenbosch.xlsx')
    
    for p in range(len(df['Property Code'])):
        # loop through properties (sync)
        prop_code = df.loc[p ,'Property Code']
        room_codes =  extractRoomCodes(df.loc[p, 'Room Codes'])
        property = Property(prop_code, p,room_codes)
        print(property.room_codes)

        for rc in room_codes:
            room = Room(rc)

            check_in = '2023-08-01'
            check_out = '2023-08-02'

            # construct payload
        
            adults = 1
            print(f'Current Room: {rc}')


            

            while str(check_in) != '2023-10-01':
                
                payload = f"establishment_id={prop_code}&start_date={formatDate(check_in)}&end_date={formatDate(check_out)}&allocation_details%5B{rc}%5D%5B1%5D%5Badults%5D={adults}&allocation_details%5B{rc}%5D%5Brooms%5D=1"
                response = requests.request("POST", URL, data=payload, headers=HEADERS)

                response = response.json()
                available = 1
                if response['data']['prices']['provider'] != 'nightsbridge':
                    available = 0
                #print(response['data']['prices']['provider'])
                
                price = response['data']['prices']['basic_price']
                variant = RoomVariant(check_in, price, available)
                
                room.variants.append(variant)
                
                check_in, check_out = nextDay(check_in, check_out)
             

            property.rooms.append(room)

        
        property_data.append(property)
        print('Property Details:')
        print(property)
        break

    print(property)

    file_name = 'tests/lekke_slaap_test.pkl'
    with open(file_name, 'wb') as file: 
        pickle.dump(property, file)
        print(f'Object successfully saved to "{file_name}"')
     
            
            #getAvailability(response)



        # loop through rooms (sync)


        # loop through dates (multi threaded)


if __name__ == "__main__":
    main()
    