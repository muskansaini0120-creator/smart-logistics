import services.booking as booking
# from services.booking import ShipmentBooking
from services.customer_service import CustomerService
from services.agent_service import AgentService
from services.tracking import TrackingService
from services.attempts import DeliveryAttemptService
from services.reports import ReportService



booking_service = booking.ShipmentBooking()
customer_service = CustomerService()
agent_service = AgentService()
tracking_service = TrackingService()
attempt_service = DeliveryAttemptService()
report_service = ReportService()




def register_customer():
    print("\n--- REGISTER CUSTOMER ---")

    name=input("Enter customer name :")
    phone=input("Enter  phone  number :")
    address=input("Enter address:")
    city=input("Enter city:")
    pin_code=input("Enter pin code :")


    customer =customer_service.register_customer(
        name,phone,address,city,pin_code
        )
    
    print("Customer registered successfully!")
    print("Customer ID :",customer.id)



def register_agent():
    print("\n--- REGISTER DELIVERY AGENT ---")

    name = input("Enter agent name: ")
    phone = input("Enter phone number: ")
    address = input("Enter address: ")
    city = input("Enter service city: ")

    agent = agent_service.register_agent(
        name, phone, address, city
    )

    print("Agent registered successfully!")
    print("Agent ID:", agent.id)




def book_shipment():
    print("\n--- BOOK SHIPMENT ---")

    sender_id = input("Enter sender customer ID: ")
    receiver_id = input("Enter receiver customer ID: ")
    origin = input("Enter origin: ")
    destination = input("Enter destination: ")
    description = input("Enter parcel description: ")
    weight = float(input("Enter parcel weight (kg): "))
    if weight <= 0:
      print("Weight must be greater than zero.")
      return

    service_type = input("Service type (Standard/Express): ")
    zone = input(
        "Zone (Local/Within State/Interstate): "
    )

    fragile_input = input("Is parcel fragile? (yes/no): ").strip().lower()
    is_fragile = fragile_input.lower() == "yes"

    shipment = booking_service.book_shipment(
        sender_id,
        receiver_id,
        origin,
        destination,
        description,
        weight,
        service_type,
        zone,
        is_fragile
    )
    
    print("\nShipment booked successfully!")
    print("Tracking ID:", shipment.tracking_id)
    print("Status:", shipment.status)
    print("Total Charges: Rs.", shipment.charge_breakdown["total"])



def assign_agent():
    print("\n--- ASSIGN DELIVERY AGENT ---")

    tracking_id = input("Enter tracking ID: ")
    agent_id = input("Enter agent ID: ")
    reason = input("Enter assignment reason: ")

    shipment = agent_service.assign_agent(
        tracking_id, agent_id, reason
    )

    print("Agent assigned successfully!")
    print("Tracking ID:", shipment["tracking_id"])
    print("Assigned Agent:", shipment["assigned_agent_id"])




def track_shipment():
    print("\n--- TRACK SHIPMENT ---")

    tracking_id = input("Enter tracking ID: ")

    shipment, _ = tracking_service.get_shipment(tracking_id)

    print("\nShipment Details")
    print("Tracking ID:", shipment["tracking_id"])
    print("Sender ID:", shipment["sender_id"])
    print("Receiver ID:", shipment["receiver_id"])
    print("Origin:", shipment["origin"])
    print("Destination:", shipment["destination"])
    print("Status:", shipment["status"])
    print("Assigned Agent:", shipment.get("assigned_agent_id"))

    print("\nTracking History:")

    history = tracking_service.get_tracking_history(tracking_id)

    if not history:
        print("No tracking history available.")
    else:
        for event in history:
            print(
                event.get("old_status"),
                "->",
                event.get("new_status"),
                "|",
                event.get("timestamp"),
                "|",
                event.get("remarks", "")
            )



def update_shipment_status():
    print("\n--- UPDATE SHIPMENT STATUS ---")

    tracking_id = input("Enter tracking ID: ")

    print("\nAvailable statuses:")
    print("1. PICKED_UP")
    print("2. IN_TRANSIT")
    print("3. OUT_FOR_DELIVERY")
    print("4. DELIVERED")
    print("5. DELIVERY_FAILED")
    print("6. CANCELLED")
    print("7. RETURN_IN_TRANSIT")
    print("8. RETURNED_TO_SENDER")

    status_options = {
        "1": "PICKED_UP",
        "2": "IN_TRANSIT",
        "3": "OUT_FOR_DELIVERY",
        "4": "DELIVERED",
        "5": "DELIVERY_FAILED",
        "6": "CANCELLED",
        "7": "RETURN_IN_TRANSIT",
        "8": "RETURNED_TO_SENDER"
    }

    choice = input("Choose new status: ")

    if choice not in status_options:
        print("Invalid choice!")
        return

    new_status = status_options[choice]

    remarks = input("Enter remarks: ")
    actor = input("Enter your name/role: ") or "System"

    recipient_name = None

    if new_status == "DELIVERED":
        recipient_name = input("Enter recipient name: ")

    shipment = tracking_service.update_status(
        tracking_id=tracking_id,
        new_status=new_status,
        actor=actor,
        remarks=remarks,
        recipient_name=recipient_name
    )

    print("\nShipment status updated!")
    print("Current Status:", shipment["status"])


def show_attempt_history():
    print("\n--- DELIVERY ATTEMPT HISTORY ---")

    tracking_id = input("Enter tracking ID: ")

    history = attempt_service.get_attempt_history(tracking_id)

    if not history:
        print("No delivery attempts found.")
        return

    for attempt in history:
        print("\nAttempt Number:", attempt["attempt_number"])
        print("Agent ID:", attempt["agent_id"])
        print("Outcome:", attempt["outcome"])
        print("Reason:", attempt["reason"])
        print("Time:", attempt["timestamp"])


def show_reports():
    print("\n--- REPORTS ---")

    print("\nDaily Report:")
    print(report_service.get_daily_report())

    print("\nTotal Revenue:")
    print("Rs.", report_service.get_revenue())

    print("\nShipment Status Summary:")
    print(report_service.get_status_summary())

    print("\nDelivery Success Rate:")
    print(
        report_service.get_delivery_success_rate(),
        "%"
    )

    print("\nAgent-wise Deliveries:")
    print(report_service.get_agent_wise_deliveries())

    print("\nAverage Delivery Time:")
    print(
        report_service.get_average_delivery_time(),
        "hours"
    )

def export_reports():

    print("\n--- EXPORT REPORTS ---")

    csv_file = report_service.export_csv()
    txt_file = report_service.export_txt()
    attempts_file = report_service.export_attempts_csv()

    print("\nAll reports exported successfully!")

    print("1. Shipments CSV:", csv_file)
    print("2. Daily Report TXT:", txt_file)
    print("3. Delivery Attempts CSV:", attempts_file)

def main():

    while True:

        print("\n================================")
        print(" SMART LOGISTICS MANAGEMENT")
        print("================================")

        print("1. Register Customer")
        print("2. Register Delivery Agent")
        print("3. Book Shipment")
        print("4. Assign Agent")
        print("5. Track Shipment")
        print("6. Update Shipment Status")
        print("7. Delivery Attempt History")
        print("8. View Reports")
        print("9. Export Reports")
        print("0. Exit")

        choice = input("\nEnter your choice: ")

        try:

            if choice == "1":
                register_customer()

            elif choice == "2":
                register_agent()

            elif choice == "3":
                book_shipment()

            elif choice == "4":
                assign_agent()

            elif choice == "5":
                track_shipment()

            elif choice == "6":
                update_shipment_status()

            elif choice == "7":
                show_attempt_history()

            elif choice == "8":
                show_reports()

            elif choice == "9":
                export_reports()

            elif choice == "0":
                print("Thank you for using Smart Logistics!")
                break

            else:
                print("Invalid choice! Please try again.")

        except ValueError as error:
            print("Input Error:", error)

        except Exception as error:
            print("Error:", error)


if __name__ == "__main__":
    main()



