from models.person import Person


class DeliveryAgent(Person):

    def __init__(self, id, full_name, phone_no, address, service_city):
        super().__init__(id, full_name, phone_no, address)

        self.service_city = service_city
        self.active = True

    def display_details(self):
        print("Agent ID:", self.id)
        print("Name:", self.full_name)
        print("Phone:", self.phone_no)
        print("Address:", self.address)
        print("Service City:", self.service_city)
        print("Active:", self.active)

    def update_details(self, address=None, service_city=None):
        if address:
            self.address = address

        if service_city:
            self.service_city = service_city

    def deactivate(self):
        self.active = False