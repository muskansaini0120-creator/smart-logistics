from storage.repository import Repository

customer_repo = Repository("customers.json")

customer = {
    "id": "C001",
    "name": "Muskan",
    "phone": "9876543210"
}

customer_repo.add(customer)

print(customer_repo.get_all())

print(customer_repo.get_by_id("C001"))