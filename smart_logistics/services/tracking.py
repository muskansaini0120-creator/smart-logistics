
from datetime import datetime

from storage.repository import Repository
from services.attempts import DeliveryAttemptService

from utils.exceptions import (
    ShipmentNotFoundError,
    InvalidStatusTransitionError,
    AgentUnavailableError,
    DeliveryAttemptLimitError
)


class TrackingService:

    def __init__(self):
        self.shipment_repo = Repository("shipments.json")
        self.event_repo = Repository("events.json")
        self.attempt_service = DeliveryAttemptService()
        self.agent_repo = Repository("agents.json")

    # Find shipment
    def get_shipment(self, tracking_id):

        shipments = self.shipment_repo.get_all()

        for shipment in shipments:
            if shipment["tracking_id"] == tracking_id:
                return shipment, shipments

        raise ShipmentNotFoundError(
            f"Shipment {tracking_id} not found"
        )

    # Validate assigned agent
    def get_active_assigned_agent(self, shipment):

        agent_id = shipment.get("assigned_agent_id")

        if not agent_id:
            raise AgentUnavailableError(
                "No agent assigned to this shipment"
            )

        agents = self.agent_repo.get_all()

        for agent in agents:

            if agent["id"] == agent_id:

                if not agent.get("active", True):
                    raise AgentUnavailableError(
                        "Assigned agent is inactive"
                    )

                return agent

        raise AgentUnavailableError(
            "Assigned agent not found"
        )

    # Update shipment status
    def update_status(
        self,
        tracking_id,
        new_status,
        actor="System",
        remarks="",
        agent_id=None,
        recipient_name=None
    ):

        # Step 1: Find shipment
        shipment, shipments = self.get_shipment(tracking_id)

        old_status = shipment["status"]

        # Step 2: Allowed transitions
        allowed_transitions = {
            "BOOKED": ["PICKED_UP", "CANCELLED"],
            "PICKED_UP": ["IN_TRANSIT"],
            "IN_TRANSIT": ["OUT_FOR_DELIVERY"],
            "OUT_FOR_DELIVERY": ["DELIVERED", "DELIVERY_FAILED"],
            "DELIVERY_FAILED": ["OUT_FOR_DELIVERY"],
            "RETURN_INITIATED": ["RETURN_IN_TRANSIT"],
            "RETURN_IN_TRANSIT": ["RETURNED_TO_SENDER"]
        }

        if new_status not in allowed_transitions.get(old_status, []):

            raise InvalidStatusTransitionError(
                f"Invalid status transition: {old_status} to {new_status}"
            )

        # Step 3: Validate agent
        if new_status in [
            "OUT_FOR_DELIVERY",
            "DELIVERY_FAILED",
            "DELIVERED"
        ]:

            assigned_agent = self.get_active_assigned_agent(shipment)

            if agent_id is not None and agent_id != assigned_agent["id"]:

                raise AgentUnavailableError(
                    "Only the assigned agent can update delivery status"
                )

            agent_id = assigned_agent["id"]

        # Step 4: Validate successful delivery
        if new_status == "DELIVERED":

            if not recipient_name or not recipient_name.strip():

                raise ValueError(
                    "Recipient name is required for successful delivery"
                )

            # Record successful attempt
            self.attempt_service.record_attempt(
                tracking_id=tracking_id,
                agent_id=agent_id,
                outcome="SUCCESS",
                reason="Delivered successfully"
            )

            shipment["recipient_name"] = recipient_name.strip()
            shipment["delivered_at"] = datetime.now().isoformat()

        # Step 5: Record failed delivery
        if new_status == "DELIVERY_FAILED":

            self.attempt_service.record_attempt(
                tracking_id=tracking_id,
                agent_id=agent_id,
                outcome="FAILED",
                reason=remarks
            )

            failed_count = self.attempt_service.get_failed_attempt_count(
                tracking_id
            )

            # Return after 3 failed attempts
            if failed_count >= self.attempt_service.MAX_ATTEMPTS:
                new_status = "RETURN_INITIATED"

        # Step 6: Update status
        shipment["status"] = new_status

        self.shipment_repo.save_data(shipments)

        # Step 7: Save event
        event = {
            "tracking_id": tracking_id,
            "old_status": old_status,
            "new_status": new_status,
            "actor": actor,
            "agent_id": agent_id,
            "timestamp": datetime.now().isoformat(),
            "remarks": remarks
        }

        self.event_repo.add(event)

        return shipment

    # Get tracking history
    def get_tracking_history(self, tracking_id):

        events = self.event_repo.get_all()

        return [
            event for event in events
            if event["tracking_id"] == tracking_id
        ]
