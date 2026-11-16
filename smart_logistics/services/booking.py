
from models.shipment import Shipment
from storage.repository import Repository
from services.pricing import PricingService


class ShipmentBooking:
    def __init__(self):
        self.shipment_repo = Repository("shipments.json")
        self.customer_repo = Repository("customers.json")
        self.pricing_service = PricingService()

    def generate_tracking_id(self):
        shipments = self.shipment_repo.get_all()

        numbers = [
            int(item["tracking_id"][3:])
            for item in shipments
        ]

        next_number = max(numbers, default=0) + 1
        return f"SHP{next_number:06d}"

    def book_shipment(
        self,
        sender_id,
        receiver_id,
        origin,
        destination,
        parcel_description,
        weight,
        service_type,
        zone,
        is_fragile=False
    ):
        customers = self.customer_repo.get_all()

        customer_ids = [
            customer["id"]
            for customer in customers
            if customer.get("active", True)
        ]

        if sender_id not in customer_ids:
            raise ValueError("Invalid or inactive sender ID")

        if receiver_id not in customer_ids:
            raise ValueError("Invalid or inactive receiver ID")

        weight = float(weight)

        if weight <= 0:
            raise ValueError("Weight must be greater than zero")

        service_type = service_type.title()

        if service_type not in ["Standard", "Express"]:
            raise ValueError("Invalid service type")

        charge_breakdown = self.pricing_service.calculate_price(
            weight, service_type, zone, is_fragile
        )

        tracking_id = self.generate_tracking_id()

        shipment = Shipment(
            tracking_id,
            sender_id,
            receiver_id,
            origin,
            destination,
            parcel_description,
            weight,
            service_type,
            zone,
            is_fragile
        )

        shipment.charge_breakdown = charge_breakdown

        self.shipment_repo.add(shipment.to_dict())

        return shipment
