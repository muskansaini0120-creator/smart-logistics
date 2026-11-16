
from datetime import datetime

from storage.repository import Repository
from utils.exceptions import DeliveryAttemptLimitError


class DeliveryAttemptService:

    MAX_ATTEMPTS = 3

    def __init__(self):
        self.attempt_repo = Repository("attempts.json")

    def record_attempt(self, tracking_id, agent_id, outcome, reason=""):

        if outcome not in ["SUCCESS", "FAILED"]:
            raise ValueError("Invalid attempt outcome")

        attempts = self.attempt_repo.get_all()

        shipment_attempts = [
            attempt for attempt in attempts
            if attempt["tracking_id"] == tracking_id
        ]

        failed_count = sum(
            1 for attempt in shipment_attempts
            if attempt["outcome"] == "FAILED"
        )

        if outcome == "FAILED" and failed_count >= self.MAX_ATTEMPTS:
            raise DeliveryAttemptLimitError(
                "Maximum 3 failed delivery attempts reached"
            )

        attempt_number = len(shipment_attempts) + 1

        new_attempt = {
            "tracking_id": tracking_id,
            "attempt_number": attempt_number,
            "agent_id": agent_id,
            "outcome": outcome,
            "reason": reason,
            "timestamp": datetime.now().isoformat()
        }

        self.attempt_repo.add(new_attempt)

        return new_attempt

    def get_attempt_history(self, tracking_id):

        attempts = self.attempt_repo.get_all()

        return [
            attempt for attempt in attempts
            if attempt["tracking_id"] == tracking_id
        ]

    def get_failed_attempt_count(self, tracking_id):

        attempts = self.get_attempt_history(tracking_id)

        return sum(
            1 for attempt in attempts
            if attempt["outcome"] == "FAILED"
        )

