import re
import datetime

def getCheckOutDate(date_in, step = 1):
        '''used when minumum stay is more than one night'''

        date_in =  datetime.datetime.strptime(date_in, "%Y-%m-%d")
        
        date_out = date_in + datetime.timedelta(days=step)
        date_out =  date_out.strftime("%Y-%m-%d") 
        
        return date_out

    
def nextDay(date_in, date_out):
    '''Get the datetime strings of the next day of both check in and check out dates'''

    date_in =  datetime.datetime.strptime(date_in, "%Y-%m-%d")
    date_out =  datetime.datetime.strptime(date_out, "%Y-%m-%d")
    
    date_in = date_in + datetime.timedelta(days=1)
    date_out = date_out + datetime.timedelta(days=1)
    
    date_in = date_in.strftime("%Y-%m-%d") 
    date_out = date_out.strftime("%Y-%m-%d") 
    
    return date_in, date_out

def formatDate(date):
    '''Get dates in special lekkeslaap price api format'''

    _date = datetime.datetime.strptime(date, "%Y-%m-%d")
    _date = _date.strftime("%Y-%b-%d") 

    _day = _date.split('-')[2]
    _month = _date.split('-')[1]
    _year = _date.split('-')[0]

    return f'{_day}%20{_month}%20{_year}'

def formatDateQ(date):
    '''Get dates in special lekkeslaap content api format'''

    _date = datetime.datetime.strptime(date, "%Y-%m-%d")
    _date = _date.strftime("%Y-%b-%d") 

    _day = _date.split('-')[2]
    _month = _date.split('-')[1]
    _year = _date.split('-')[0]

    return f'{_day} {_month} {_year}'

def formatDateQRev(date):
    '''Get dates in special lekkeslaap content api format'''

    _date = datetime.datetime.strptime(date, "%Y %b %d")
    _date = _date.strftime("%Y-%m-%d") 


    return _date


def getCancelDiff(date, date_pol):

    if date_pol == '':
        return 0

    date =  datetime.datetime.strptime(date, "%Y-%m-%d")
    date_pol =  datetime.datetime.strptime(date_pol, "%d %b %Y")

    date_delta = date_pol - date
    return date_delta.days






def extractRoomCodes(room_codes):
    '''Extract list of room codes from stringed list in excel'''

    return re.findall(r'\d+', room_codes)


