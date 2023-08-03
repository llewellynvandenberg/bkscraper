import requests
import requests
import json
import asyncio
import aiohttp
import time

import urllib.parse

URL = "https://www.booking.com/hotel/za/three-bridges-b-amp-b.en-gb.html"
print(time.perf_counter())
check_in = '2023-08-01'
check_out = '2023-08-02'

querystring = {"aid":"376363","label":"booking-name-9wTEEbDxZqFKYE7yVIQi0QS540988882221:pl:ta:p1:p22,563,000:ac:ap:neg:fi:tikwd-51481728:lp1028743:li:dec:dm:ppccp=UmFuZG9tSVYkc2RlIyh9YfqnDqqG8nt1XFzPnqOODws","sid":"b1eb98c644314edb8245ce0e87657812","all_sr_blocks":f"173676704_95713960_1_1_0;checkin={check_in};checkout={check_out};dest_id=-1237509;dest_type=city;dist=0;group_adults=1;group_children=0;hapos=2;highlighted_blocks=173676704_95713960_1_1_0;hpos=2;matching_block_id=173676704_95713960_1_1_0;no_rooms=1;req_adults=1;req_children=0;room1=A;sb_price_type=total;sr_order=popularity;sr_pri_blocks=173676704_95713960_1_1_0__61750;srepoch=1688030328;srpvid=a11c417b697d000b;type=total;ucfs=1"}

payload = ""
headers = {
    "authority": "www.booking.com",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
    "cache-control": "max-age=0",
    "sec-ch-ua": '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
}

#response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

reqs = []
import datetime
def nextDay(date_in, date_out):
    '''Get the datetime strings of the next day of both check in and check out dates'''

    date_in =  datetime.datetime.strptime(date_in, "%Y-%m-%d")
    date_out =  datetime.datetime.strptime(date_out, "%Y-%m-%d")
    
    date_in = date_in + datetime.timedelta(days=1)
    date_out = date_out + datetime.timedelta(days=1)
    
    date_in = date_in.strftime("%Y-%m-%d") 
    date_out = date_out.strftime("%Y-%m-%d") 
    
    return date_in, date_out


check_in = '2023-08-01'
check_out = '2023-08-02'

while 1:
    
    if check_in == '2023-11-01':
        break

    querystring = {"aid":"376363","label":"booking-name-9wTEEbDxZqFKYE7yVIQi0QS540988882221:pl:ta:p1:p22,563,000:ac:ap:neg:fi:tikwd-51481728:lp1028743:li:dec:dm:ppccp=UmFuZG9tSVYkc2RlIyh9YfqnDqqG8nt1XFzPnqOODws","sid":"b1eb98c644314edb8245ce0e87657812","all_sr_blocks":f"173676704_95713960_1_1_0;checkin={check_in};checkout={check_out};dest_id=-1237509;dest_type=city;dist=0;group_adults=1;group_children=0;hapos=2;highlighted_blocks=173676704_95713960_1_1_0;hpos=2;matching_block_id=173676704_95713960_1_1_0;no_rooms=1;req_adults=1;req_children=0;room1=A;sb_price_type=total;sr_order=popularity;sr_pri_blocks=173676704_95713960_1_1_0__61750;srepoch=1688030328;srpvid=a11c417b697d000b;type=total;ucfs=1"}

    reqs.append(querystring)
    
    check_in, check_out = nextDay(check_in, check_out)


async def get_data(session, url):
    async with session.request("GET", URL, data=payload, headers=headers, params=url) as resp:
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


resp = asyncio.run(main(reqs))
print(time.perf_counter())
for r in range(len(resp)):
    print(resp[r][1000:1020])