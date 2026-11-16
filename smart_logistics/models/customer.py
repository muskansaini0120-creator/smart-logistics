
from models.person import Person


class Customer(Person):
    def __init__(self, id, full_name, phone_no, address, city, pin_code):
        super().__init__(id, full_name, phone_no, address)
        self.city = city
        self.pin_code = pin_code
        self.active = True

    def display_details(self):
        print(self.id)
        print(self.full_name)
        print(self.phone_no)
        print(self.address)
        print(self.city)
        print(self.pin_code)

    
    def update_details(self, phone_no=None, address=None, city=None, pin_code=None):
        if phone_no is not None:
            self.phone_no = phone_no

        if address is not None:
            self.address = address

        if city is not None:
            self.city = city

        if pin_code is not None:
            self.pin_code = pin_code


    def to_dict(self):
     return {
        "id": self.id,
        "full_name": self.full_name,
        "phone_no": self.phone_no,
        "address": self.address,
        "city": self.city,
        "pin_code": self.pin_code,
        "active": self.active
    }