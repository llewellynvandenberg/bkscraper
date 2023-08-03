'''Get property codes and names from search pages'''




import requests
import pandas as pd
import json

AREA = 'kruger-to-canyons'



payload = ""
headers = {
    "cookie": "language_preference=en; PHPSESSID=oq9s4qmt9ltjalnj7bcgmkuc57; SOURCES_ALL=%255B%255B1688997463%252C%2522other%2522%252C%2522%255C%252Faccommodation-in%255C%252Fstellenbosch%255C%252F2%2522%252C%2522%2522%252C%2522%2522%252C%2522%2522%255D%255D",
    "authority": "www.lekkeslaap.co.za",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
    "cache-control": "max-age=0",
    "referer": f"https://www.lekkeslaap.co.za/accommodation-in/{AREA}?sort=recommended&start=2023-12-01&end=2023-12-02&pax=2",
    "sec-ch-ua": '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}





page = 1
page_max = 20
property_codes = []
property_names = []
property_ratings = []
while 1:
    if page > page_max:
        break
    print(page)


    try:
        url = f"https://www.lekkeslaap.co.za/accommodation-in/{AREA}/{page}"

        response = requests.request("GET", url, data=payload, headers=headers)

        response = str(response.text)

        # find rating
        rat_resp = response.split('rating-stars position-absolute\" style=\"white-space:nowrap; width: ')        
        temp_rats = []
        cnt  = 0
        for rat in rat_resp:
            
            try:
                rating  = int(rat[:2])
                property_ratings.append(rating)
                
            except:
                pass
            
            
            for i in range((len(rat.split('establishment-item__description')))-2):
                property_ratings.append('')
            cnt +=1

            if cnt == len(rat_resp):
                for i in range((len(rat.split('establishment-item__description')))-1):
                    property_ratings.append('')

            
                
        


        # find json object in text
        response = response.split('let data = ')[1].split('if (false && window')[0]
        response = json.loads(response)

        if len(response['establishments']) < 1:
            break

        for prop in response['establishments']:
            tmp_prop = response['establishments'][prop]
            property_codes.append(tmp_prop['establishment_id'])
            property_names.append(tmp_prop['name'])
        page+=1
    except:
        break

# text_file = open("sample.txt", "w")
# n = text_file.write('Welcome to pythonexamples.org')
# text_file.close()

df = pd.DataFrame({
    'property_code' : property_codes,
    'property_name' : property_names,
    'property_rating' : property_ratings
})

df.to_csv('data/LekkeSlaap_Kruger_metadata.csv')