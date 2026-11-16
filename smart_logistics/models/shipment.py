
from datetime import datetime


class Shipment:
    def __init__(
        self,
        tracking_id,
        sender_id,
        receiver_id,
        origin,
        destination,
        parcel_description,
        weight,
        service_type,
        zone,
        is_fragile=False,
        declared_value=None
    ):
        self.tracking_id = tracking_id
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.origin = origin
        self.destination = destination
        self.parcel_description = parcel_description
        self.weight = weight
        self.service_type = service_type
        self.zone = zone
        self.is_fragile = is_fragile
        self.booked_at = datetime.now().isoformat()
        self.declared_value = declared_value
        self.status = "BOOKED"
        self.charge_breakdown = {}
        self.assigned_agent_id = None

    def to_dict(self):
        return {
            "tracking_id": self.tracking_id,
            "sender_id": self.sender_id,
            "receiver_id": self.receiver_id,
            "origin": self.origin,
            "destination": self.destination,
            "parcel_description": self.parcel_description,
            "weight": self.weight,
            "service_type": self.service_type,
            "zone": self.zone,
            "is_fragile": self.is_fragile,
            "booked_at": self.booked_at,
            "declared_value": self.declared_value,
            "status": self.status,
            "charge_breakdown": self.charge_breakdown,
            "assigned_agent_id": self.assigned_agent_id
        }

    @classmethod
    def from_dict(cls, data):
        shipment = cls(
            data["tracking_id"],
            data["sender_id"],
            data["receiver_id"],
            data["origin"],
            data["destination"],
            data["parcel_description"],
            data["weight"],
            data["service_type"],
            data.get("zone", "Local"),
            data.get("is_fragile", False),
            data.get("declared_value")
        )

        shipment.booked_at = data.get("booked_at", shipment.booked_at)
        shipment.status = data.get("status", "BOOKED")
        shipment.charge_breakdown = data.get("charge_breakdown", {})
        shipment.assigned_agent_id = data.get("assigned_agent_id")

        return shipment
