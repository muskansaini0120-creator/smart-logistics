
import csv
import os
from datetime import datetime, date

from storage.repository import Repository


class ReportService:

    def __init__(self):
        self.shipment_repo = Repository("shipments.json")
        self.attempt_repo = Repository("attempts.json")
        self.agent_repo = Repository("agents.json")

    def get_daily_report(self):
        shipments = self.shipment_repo.get_all()
        attempts = self.attempt_repo.get_all()

        today = date.today().isoformat()

        daily_shipments = [
            s for s in shipments
            if s.get("booked_at", "").startswith(today)
        ]

        daily_attempts = [
            a for a in attempts
            if a.get("timestamp", "").startswith(today)
        ]

        return {
            "date": today,
            "bookings": len(daily_shipments),
            "deliveries": sum(
                1 for s in shipments
                if s.get("delivered_at", "").startswith(today)
            ),
            "failed_attempts": sum(
                1 for a in daily_attempts
                if a.get("outcome") == "FAILED"
            ),
            "pending": sum(
                1 for s in shipments
                if s.get("status") not in [
                    "DELIVERED", "CANCELLED", "RETURNED_TO_SENDER"
                ]
            ),
            "returns": sum(
                1 for s in shipments
                if s.get("status") in [
                    "RETURN_INITIATED",
                    "RETURN_IN_TRANSIT",
                    "RETURNED_TO_SENDER"
                ]
            )
        }

    def get_revenue(self):
        shipments = self.shipment_repo.get_all()

        return sum(
            s.get("charge_breakdown", {}).get("total", 0)
            for s in shipments
        )

    def get_status_summary(self):
        shipments = self.shipment_repo.get_all()
        summary = {}

        for shipment in shipments:
            status = shipment.get("status", "UNKNOWN")
            summary[status] = summary.get(status, 0) + 1

        return summary

    def get_delivery_success_rate(self):
        attempts = self.attempt_repo.get_all()

        total = len(attempts)

        if total == 0:
            return 0

        successful = sum(
            1 for attempt in attempts
            if attempt.get("outcome") == "SUCCESS"
        )

        return round((successful / total) * 100, 2)

    def get_agent_wise_deliveries(self):
        attempts = self.attempt_repo.get_all()
        agents = self.agent_repo.get_all()

        report = {}

        for agent in agents:
            agent_id = agent["id"]
            report[agent_id] = {
                "agent_name": agent["full_name"],
                "deliveries": 0
            }

        for attempt in attempts:
            if attempt.get("outcome") == "SUCCESS":
                agent_id = attempt.get("agent_id")

                if agent_id in report:
                    report[agent_id]["deliveries"] += 1

        return report

    def get_average_delivery_time(self):
        shipments = self.shipment_repo.get_all()

        delivery_times = []

        for shipment in shipments:
            if (
                shipment.get("status") == "DELIVERED"
                and shipment.get("booked_at")
                and shipment.get("delivered_at")
            ):
                booked = datetime.fromisoformat(shipment["booked_at"])
                delivered = datetime.fromisoformat(shipment["delivered_at"])

                hours = (delivered - booked).total_seconds() / 3600
                delivery_times.append(hours)

        if not delivery_times:
            return 0

        return round(sum(delivery_times) / len(delivery_times), 2)

    
    def export_csv(self):
        shipments = self.shipment_repo.get_all()

        os.makedirs("reports", exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = f"reports/shipments_{timestamp}.csv"

        # Collect all fields from every shipment
        fieldnames = []

        for shipment in shipments:
            for key in shipment.keys():
                if key not in fieldnames:
                    fieldnames.append(key)

        if not fieldnames:
            fieldnames = ["tracking_id", "status"]

        with open(file_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=fieldnames,
                extrasaction="ignore"
            )

            writer.writeheader()
            writer.writerows(shipments)

        return file_path


    def export_txt(self):
        os.makedirs("reports", exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = f"reports/daily_report_{timestamp}.txt"

        daily = self.get_daily_report()
        status = self.get_status_summary()
        revenue = self.get_revenue()
        success_rate = self.get_delivery_success_rate()
        average_time = self.get_average_delivery_time()
        agent_report = self.get_agent_wise_deliveries()

        with open(file_path, "w", encoding="utf-8") as file:
            file.write("SMART LOGISTICS REPORT\n")
            file.write("======================\n\n")

            file.write(f"Date: {daily['date']}\n")
            file.write(f"Today's Bookings: {daily['bookings']}\n")
            file.write(f"Today's Deliveries: {daily['deliveries']}\n")
            file.write(f"Today's Failed Attempts: {daily['failed_attempts']}\n")
            file.write(f"Pending Shipments: {daily['pending']}\n")
            file.write(f"Returns: {daily['returns']}\n\n")

            file.write(f"Total Revenue: Rs. {revenue}\n")
            file.write(f"Delivery Success Rate: {success_rate}%\n")
            file.write(f"Average Delivery Time: {average_time} hours\n\n")

            file.write("STATUS SUMMARY\n")

            for key, value in status.items():
                file.write(f"{key}: {value}\n")

            file.write("\nAGENT-WISE DELIVERIES\n")

            for agent_id, details in agent_report.items():
                file.write(
                    f"{agent_id} - {details['agent_name']}: "
                    f"{details['deliveries']}\n"
                )

        return file_path


    
     
    def export_attempts_csv(self):

        attempts = self.attempt_repo.get_all()

        os.makedirs("reports", exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        file_path = f"reports/attempts_{timestamp}.csv"

        fieldnames = [
            "tracking_id",
            "attempt_number",
            "agent_id",
            "outcome",
            "reason",
            "timestamp"
        ]

        with open(file_path, "w", newline="", encoding="utf-8") as file:

            writer = csv.DictWriter(file, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerows(attempts)

        return file_path
