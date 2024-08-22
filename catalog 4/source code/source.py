import datetime

class ChargingStation:
    def __init__(self, name, location, slots):
        self.name = name
        self.location = location
        self.slots = slots
        self.bookings = {}

    def find_available_slot(self, date):
        available_slots = [slot for slot in self.slots if date not in self.bookings.get(slot, [])]
        return available_slots

    def book_slot(self, slot, date):
        if slot in self.find_available_slot(date):
            if slot not in self.bookings:
                self.bookings[slot] = []
            self.bookings[slot].append(date)
            print(f"Slot {slot} booked successfully on {date} at {self.name}!")
            return True
        else:
            print(f"Slot {slot} is already booked on {date} at {self.name}.")
            return False

    def get_booked_slots(self):
        return self.bookings


class EVChargingSystem:
    def __init__(self):
        self.stations = []

    def add_station(self, name, location, slots):
        station = ChargingStation(name, location, slots)
        self.stations.append(station)

    def find_stations_by_location(self, location):
        return [station for station in self.stations if station.location.lower() == location.lower()]

    def filter_stations(self, location=None):
        if location:
            return self.find_stations_by_location(location)
        return self.stations


def main():
    system = EVChargingSystem()

    # Adding charging stations
    system.add_station("Station A", "Downtown", ["Slot 1", "Slot 2", "Slot 3"])
    system.add_station("Station B", "Uptown", ["Slot 1", "Slot 2"])
    system.add_station("Station C", "Suburb", ["Slot 1", "Slot 2", "Slot 3", "Slot 4"])

    while True:
        # Main menu options
        print("\nWelcome to the EV Charging Station Finder and Slot Booking System!")
        print("1. View all charging stations")
        print("2. Search for stations by location")
        print("3. Quit")

        choice = input("Please select an option (1/2/3): ")

        if choice == "1":
            stations = system.filter_stations()
        elif choice == "2":
            location = input("Enter the location to find stations: ")
            stations = system.filter_stations(location)
        elif choice == "3":
            print("Thank you for using the system. Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")
            continue

        if stations:
            print(f"\nAvailable stations:")
            for station in stations:
                print(f"- {station.name} ({station.location})")

            # User selects a station to book a slot
            station_name = input("Enter the station name to book a slot: ")
            selected_station = next((s for s in stations if s.name.lower() == station_name.lower()), None)

            if selected_station:
                # User inputs the date for booking
                date_input = input("Enter the date for booking (YYYY-MM-DD) or press Enter for today's date: ")
                if date_input:
                    try:
                        date = datetime.datetime.strptime(date_input, "%Y-%m-%d").date()
                    except ValueError:
                        print("Invalid date format. Please try again.")
                        continue
                else:
                    date = datetime.date.today()

                # Check available slots and book
                available_slots = selected_station.find_available_slot(date)
                if available_slots:
                    print(f"Available slots on {date}: {', '.join(available_slots)}")
                    slot_to_book = input("Enter the slot you want to book: ")
                    selected_station.book_slot(slot_to_book, date)
                else:
                    print("No available slots for the selected date.")
            else:
                print(f"No station found with the name '{station_name}'. Please try again.")
        else:
            print(f"No charging stations found.")

        # Ask if the user wants to book another slot or quit
        another_booking = input("\nDo you want to book another slot or search again? (yes to continue, no to quit): ")
        if another_booking.lower() != "yes":
            print("Thank you for using the system. Goodbye!")
            break


if __name__ == "__main__":
    main()
