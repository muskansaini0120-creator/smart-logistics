
from models.agent import DeliveryAgent
from storage.repository import Repository
from datetime import datetime


class AgentService:

    def __init__(self):
        self.agent_repo = Repository("agents.json")
        self.shipment_repo = Repository("shipments.json")
        self.event_repo = Repository("events.json")

    def generate_agent_id(self):
        agents = self.agent_repo.get_all()

        numbers = [
            int(agent["id"][2:])
            for agent in agents
            if agent["id"].startswith("AG")
        ]

        next_number = max(numbers, default=0) + 1

        return f"AG{next_number:04d}"

    def register_agent(self, full_name, phone_no, address, service_city):

        phone_no = str(phone_no)

        if not phone_no.isdigit() or len(phone_no) != 10:
            raise ValueError("Phone number must contain 10 digits")

        if not full_name.strip():
            raise ValueError("Agent name cannot be empty")

        agents = self.agent_repo.get_all()

        for agent in agents:
            if agent["phone_no"] == phone_no:
                raise ValueError("Agent phone number already exists")

        agent_id = self.generate_agent_id()

        agent = DeliveryAgent(
            agent_id,
            full_name,
            phone_no,
            address,
            service_city
        )

        self.agent_repo.add({
            "id": agent.id,
            "full_name": agent.full_name,
            "phone_no": agent.phone_no,
            "address": agent.address,
            "service_city": agent.service_city,
            "active": agent.active
        })

        return agent

    def get_agent(self, agent_id):

        agent = self.agent_repo.get_by_id(agent_id)

        if agent is None:
            raise ValueError("Agent not found")

        return agent

    def get_all_agents(self):
        return self.agent_repo.get_all()

    def deactivate_agent(self, agent_id):

        agents = self.agent_repo.get_all()

        for agent in agents:
            if agent["id"] == agent_id:

                agent["active"] = False

                self.agent_repo.save_data(agents)

                return True

        raise ValueError("Agent not found")

    def activate_agent(self, agent_id):

        agents = self.agent_repo.get_all()

        for agent in agents:
            if agent["id"] == agent_id:

                agent["active"] = True

                self.agent_repo.save_data(agents)

                return True

        raise ValueError("Agent not found")

    def assign_agent(
        self,
        tracking_id,
        agent_id,
        reason="Initial assignment"
    ):

        # Step 1: Check agent
        agent = self.get_agent(agent_id)

        if not agent["active"]:
            raise ValueError("Cannot assign an inactive agent")

        # Step 2: Find shipment
        shipments = self.shipment_repo.get_all()

        shipment = None

        for item in shipments:
            if item["tracking_id"] == tracking_id:
                shipment = item
                break

        if shipment is None:
            raise ValueError("Shipment not found")

        # Step 3: Check shipment status
        non_assignable_statuses = [
            "RETURN_INITIATED",
            "RETURN_IN_TRANSIT",
            "RETURNED_TO_SENDER",
            "DELIVERED",
            "CANCELLED"
        ]

        if shipment["status"] in non_assignable_statuses:
            raise ValueError(
                "Cannot assign agent to a completed or return shipment"
            )

        # Step 4: Save previous agent ID
        old_agent_id = shipment.get("assigned_agent_id")

        # Step 5: Assign new agent
        shipment["assigned_agent_id"] = agent_id

        self.shipment_repo.save_data(shipments)

        # Step 6: Record assignment event
        event = {
            "tracking_id": tracking_id,
            "event_type": "AGENT_ASSIGNED",
            "old_agent_id": old_agent_id,
            "new_agent_id": agent_id,
            "actor": "System",
            "timestamp": datetime.now().isoformat(),
            "remarks": reason
        }

        self.event_repo.add(event)

        return shipment


