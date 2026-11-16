from abc import ABC, abstractmethod


class Person(ABC):

    def __init__(self, id, full_name, phone_no, address):
        self.id = id
        self.full_name = full_name
        self.phone_no = phone_no
        self.address = address

    @abstractmethod
    def display_details(self):
        pass






