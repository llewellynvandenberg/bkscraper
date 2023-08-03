SITE = 'Lekke Slaap'
### classes
class Property:
    def __init__(self, prop_code, prop_ID, prop_name, prop_rating) -> None:
        self.site = SITE
        self.nr_rooms = 0
        self.prop_code = prop_code
        self.prop_ID = prop_ID
        self.prop_name = prop_name
        self.prop_rating = prop_rating
        self.rooms = []

    def to_dict(self):
        self.nr_rooms = len(self.rooms)
        
        dict = {
            'site': self.site,
            'prop_code': self.prop_code,
            'prop_ID': self.prop_ID,
            'prop_name': self.prop_name,
            'rating' : self.prop_rating,
            'rooms':[x.to_dict() for x in self.rooms]
        }
        return dict

class Room:
    def __init__(self, room_code, room_name, beds, occupency, child_pol, cancel_pol, min_nights = 0) -> None:
        self.room_code = room_code # ['id']
        self.occupency = occupency # ['sleeps']['adults']
        self.room_name = room_name # ['name']
        self.cancel_pol = cancel_pol # ['free_cancellation_promotion']['deadline'] ""==None
        self.beds = beds # ['bed']
        self.variants = [] 
        self.child_pol = child_pol # ['minimum_child_age'] -1==None

    def to_dict(self):

        dict = {
            'room_code': self.room_code,
            'occupency': self.occupency,
            'room_name': self.room_name,
            'cancel_pol': self.cancel_pol,
            'child_pol': self.child_pol,
            'beds': self.beds,
            'variants': [vars(x) for x in self.variants]
        }
        return dict

        
class RoomVariant:
    def __init__(self, date, price, price_2,availability, party_size, nights = 1) -> None:
        self.date = date 
        self.price = price # ['price']['from']['final_price']
        self.price_2 = price_2
        self.nights = nights 
        self.availability = availability # ['availability']
        self.party_size = party_size # ['price']['for']