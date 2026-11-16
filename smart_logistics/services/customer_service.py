
from models.customer import Customer
from storage.repository import Repository
from utils.exceptions import CustomerNotFoundError


class CustomerService:

    def __init__(self):
        self.customer_repo = Repository("customers.json")

    def generate_customer_id(self):
        customers = self.customer_repo.get_all()

        numbers = [
            int(customer["id"][1:])
            for customer in customers
            if customer["id"].startswith("C")
            and customer["id"][1:].isdigit()
        ]

        next_number = max(numbers, default=0) + 1
        return f"C{next_number:03d}"

    def register_customer(
        self, full_name, phone_no, address, city, pin_code
    ):
        phone_no = str(phone_no)

        if not full_name.strip():
            raise ValueError("Customer name cannot be empty")

        if not phone_no.isdigit() or len(phone_no) != 10:
            raise ValueError("Phone number must contain 10 digits")

        customers = self.customer_repo.get_all()

        for customer in customers:
            if customer["phone_no"] == phone_no:
                raise ValueError("Phone number already exists")

        customer_id = self.generate_customer_id()

        customer = Customer(
            customer_id, full_name, phone_no,
            address, city, pin_code
        )

        self.customer_repo.add(customer.to_dict())

        return customer

    def get_customer(self, customer_id):
        customer = self.customer_repo.get_by_id(customer_id)

        if customer is None:
            raise CustomerNotFoundError("Customer not found")

        return customer

    def get_all_customers(self):
        return self.customer_repo.get_all()

    def update_customer(
        self, customer_id, address=None, city=None, pin_code=None
    ):
        customers = self.customer_repo.get_all()

        for customer in customers:
            if customer["id"] == customer_id:

                if address:
                    customer["address"] = address

                if city:
                    customer["city"] = city

                if pin_code:
                    customer["pin_code"] = pin_code

                self.customer_repo.save_data(customers)
                return customer

        raise CustomerNotFoundError("Customer not found")

    def deactivate_customer(self, customer_id):
        customers = self.customer_repo.get_all()

        for customer in customers:
            if customer["id"] == customer_id:
                customer["active"] = False
                self.customer_repo.save_data(customers)
                return True

        raise CustomerNotFoundError("Customer not found")

    def activate_customer(self, customer_id):
        customers = self.customer_repo.get_all()

        for customer in customers:
            if customer["id"] == customer_id:
                customer["active"] = True
                self.customer_repo.save_data(customers)
                return True

        raise CustomerNotFoundError("Customer not found")
