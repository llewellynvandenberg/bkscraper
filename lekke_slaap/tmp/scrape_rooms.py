##
## This file contains the function to scrape room details
##
import requests
import pandas as pd
from datetime import datetime


URL = "https://www.lekkeslaap.co.za/forms/new_enquiry_form/backend/details.php"


PAYLOAD = ""
HEADERS = {
    "cookie": "_gcl_au=1.1.354445611.1687193007; _fbp=fb.2.1687193007238.767402674; language_preference=en; SOURCES_ALL=%5B%5B1687193004%2C%22google%22%2C%22%5C%2F%22%2C%22%22%2C%22%22%2C%22%22%5D%2C%5B1687193006%2C%22PAID_AdWords%22%2C%22%5C%2F%3Fppc%3DAdWords_LSbrand%26gclid%3DCjwKCAjw-b-kBhB-EiwA4fvKrOQJUHWBtGA4CUIIVvrJVedMco05UdSWvMNVrMuvJiOut_MwJJlHGhoCb9EQAvD_BwE%22%2C%22%22%2C%22LSbrand%22%2C%22%22%5D%2C%5B1687364403%2C%22google%22%2C%22%5C%2F%22%2C%22%22%2C%22%22%2C%22%22%5D%2C%5B1687364404%2C%22PAID_AdWords%22%2C%22%5C%2F%3Fppc%3DAdWords_LSbrand%26gclid%3DCjwKCAjwv8qkBhAnEiwAkY-ahnaWH1G0Rb6XDqbxLg1lX8pY0VmReJxevY57h2rsQ89544wOQZ7OtBoCArIQAvD_BwE%22%2C%22%22%2C%22LSbrand%22%2C%22%22%5D%2C%5B1687966340%2C%22google%22%2C%22%5C%2F%22%2C%22%22%2C%22%22%2C%22%22%5D%2C%5B1687966341%2C%22PAID_AdWords%22%2C%22%5C%2F%3Fppc%3DAdWords_LSbrand%26gclid%3DCj0KCQjwtO-kBhDIARIsAL6Lorc7KvdnZ5hWg4TcNvhsBCm-PsgzH_r1t2pi8Qh1C6gYuHry1I9kunEaAlrPEALw_wcB%22%2C%22%22%2C%22LSbrand%22%2C%22%22%5D%5D; _gac_UA-5318665-12=1.1687966343.Cj0KCQjwtO-kBhDIARIsAL6Lorc7KvdnZ5hWg4TcNvhsBCm-PsgzH_r1t2pi8Qh1C6gYuHry1I9kunEaAlrPEALw_wcB; _gcl_aw=GCL.1687966343.Cj0KCQjwtO-kBhDIARIsAL6Lorc7KvdnZ5hWg4TcNvhsBCm-PsgzH_r1t2pi8Qh1C6gYuHry1I9kunEaAlrPEALw_wcB; _gid=GA1.3.805194323.1688382766; PHPSESSID=v2rmrqg0i5vfb8f7mgkvtrcl3p; __cf_bm=n0Uff5YPfpR8Sols24kFoUfYld7kdbRbRLRjDmTKwwA-1688463412-0-AVB2QHooIsZDMbiaDafAImWZQkX7Bp+9ml1ZppZ2V6Qtjd4bxb2o8mLG6AE4qBtFfA==; _ga=GA1.1.1250577460.1687193007; recently_viewed=8958%2C1687618753%3B75267%2C1687632736%3B251%2C1688463507%3B29141%2C1687966447%3B4158%2C1687974666%3B6921%2C1687974697%3B44284%2C1687974735; _ga_SQ0J2QN79X=GS1.1.1688463412.13.1.1688463507.60.0.0",
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


def scrape_rooms(property_code):

    room_codes = []
    room_names = []

    querystring = {"start_date":"10 Sep 2023","end_date":"11 Sep 2023","id":f"{property_code}"}

    response = requests.request("GET", URL, data=PAYLOAD, headers=HEADERS, params=querystring)

    response = response.json()


    

    for res in response:
        try:
            room_codes.append(res['id'])
            room_names.append(res['name'])
        except:
            print(res)


    return {'room_codes': room_codes, 'room_names': room_names}
