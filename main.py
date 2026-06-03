#Student ID 011101442

import datetime

from hashTable import HashTable
from truckClass import Truck
from packageFileLoader import load_packages
from distanceTableLoader import load_distances
from nearestNeighbor import compute_routes
from distanceTableLoader import get_location_index


#Display the main menu to the user
def display_menu():

    print("")
    print("========================================")
    print("  WGUPS Package Tracking System")
    print("========================================")
    print("  1 - Look up a package by ID")
    print("  2 - Show all package statuses at a given time")
    print("  3 - Display total mileage for all trucks")
    print("  4 - Exit")
    print("========================================")

#User inputs a package and the program outputs all information for that package
def run_package_lookup(hash_table):

    input_value = input("Enter package ID: ")

    try:
        package_id_int = int(input_value)
    except ValueError:
        print("ERROR: '" + input_value + "' is not a valid integer. Please try again.")
        return

    found_package = hash_table.lookup(package_id_int)

    if found_package is None:
        print("Package not found.")
        return

    print("")
    print("--- Package Details ---")
    print("Package ID    : " + str(found_package.package_id))
    print("Address       : " + str(found_package.address))
    print("City          : " + str(found_package.city))
    print("ZIP Code      : " + str(found_package.zip_code))
    print("Deadline      : " + str(found_package.deadline))
    print("Weight (kg)   : " + str(found_package.weight))
    print("Special Notes : " + str(found_package.special_notes))
    print("Status        : " + str(found_package.status))
    print("Delivery Time : " + str(found_package.delivery_time))

#Update packge 9 address
def correct_package_9(hash_table):
    package = hash_table.lookup(9)
    package.address = "410 S State St"

#User inputs a time and the program outputs all packages at that time
def run_all_statuses_at_time(hash_table, trucks):
    # Display the delivery status of all packages at a user-specified time

    time_input = input("Enter time to check (HH:MM, 24-hour format): ")

    try:
        query_time = datetime.datetime.strptime(time_input, "%H:%M").time()
    except ValueError:
        print("ERROR: '" + time_input + "' is not a valid time. Please use HH:MM format (e.g. 10:30).")
        return

    all_packages = hash_table.get_all_packages()

    print("")
    print("--- All Package Statuses at " + str(query_time) + " ---")
    print("")

    for current_package in all_packages:
        package_id_str = str(current_package.package_id).zfill(2)

        if current_package.package_id == 9 and query_time < datetime.time(10, 20):
            address_str = "300 State St".ljust(25)[:25]
        else:
            address_str = str(current_package.address)

        if current_package.delivery_time is not None and current_package.delivery_time <= query_time:
            status_at_query_time = "delivered at " + str(current_package.delivery_time)
        else:
            status_at_query_time = "at hub               "
            for truck in trucks:
                if current_package in truck.packages:
                    if truck.depart_time <= query_time:
                        status_at_query_time = "en route             "
                    break

        print("ID: " + package_id_str + "  |  Status: " + status_at_query_time + "  |  Address: " + address_str)

#Calculates total mileage for all trucks at EOD
def run_total_mileage(total_mileage):

    mileage_str = str(total_mileage)
    print("Total mileage traveled by all trucks: " + mileage_str + " miles")

#Assigns all 40 packages to 3 different trucks
def load_trucks(trucks, hash_table):

    truck_1_ids = [1, 5, 7, 8, 10, 11, 12, 13, 14, 15, 16, 19, 20, 29, 30, 37]
    #truck_1_ids = []

    truck_2_ids = [3, 4, 18, 36, 38, 6, 25, 40, 31, 34, 21, 22, 23, 24]
    #truck_2_ids = []

    truck_3_ids = [9, 28, 32, 33, 35, 39, 2, 17, 26, 27]
    #truck_3_ids = []


    for package_id in truck_1_ids:
        trucks[0].packages.append(hash_table.lookup(package_id))
    for package_id in truck_2_ids:
        trucks[1].packages.append(hash_table.lookup(package_id))
    for package_id in truck_3_ids:
        trucks[2].packages.append(hash_table.lookup(package_id))

#Assigns departure times for each truck
def set_depart_times(trucks):

    trucks[0].depart_time = datetime.time(8, 0)
    trucks[1].depart_time = datetime.time(9, 5)
    trucks[2].depart_time = datetime.time(10, 45, 20)

#Simulates the delivery route for a given truck, updating mileage and package status as it goes
def run_simulation(truck, hash_table, locations, distance_matrix):

    for package in truck.packages:
        package.status = "en route"

    current_time = truck.depart_time

    for i in range(len(truck.route) - 1):
        from_index = truck.route[i]
        to_index = truck.route[i + 1]
        distance = distance_matrix[from_index][to_index]

        truck.mileage += distance
        hours = distance / 18
        current_time = (datetime.datetime.combine(datetime.date.today(), current_time) + datetime.timedelta(hours=hours)).time()

        for package in truck.packages:
            stop_index = get_location_index(package.address, locations)
            if stop_index == to_index:
                package.status = "delivered"
                package.delivery_time = current_time
    truck.return_time = current_time

#Main
if __name__ == "__main__":

    hash_table = HashTable(50)

    load_packages("PackageFile.csv", hash_table)

    locations, distance_matrix = load_distances("DistanceTable.csv")

    trucks = [Truck(1), Truck(2), Truck(3)]

    load_trucks(trucks, hash_table)

    set_depart_times(trucks)

    correct_package_9(hash_table)

    compute_routes(trucks, locations, distance_matrix)

    total_mileage = 0

    run_simulation(trucks[0], hash_table, locations, distance_matrix)

    run_simulation(trucks[1], hash_table, locations, distance_matrix)

    run_simulation(trucks[2], hash_table, locations, distance_matrix)

    total_mileage = trucks[0].mileage + trucks[1].mileage + trucks[2].mileage

    print("Truck 1 return time: " + str(trucks[0].return_time))
    print("Truck 2 return time: " + str(trucks[1].return_time))
    print("Truck 3 return time: " + str(trucks[2].return_time))

    print("")
    print("Simulation complete. Total mileage: " + str(total_mileage))

    while True:
        display_menu()

        menu_choice = input("Enter your choice (1-4): ")

        if menu_choice == "1":
            run_package_lookup(hash_table)

        elif menu_choice == "2":
            run_all_statuses_at_time(hash_table, trucks)

        elif menu_choice == "3":
            run_total_mileage(total_mileage)

        elif menu_choice == "4":
            print("Exiting WGUPS Tracking System. Goodbye.")
            break

        else:
            print(
                "ERROR: '"
                + menu_choice
                + "' is not a valid choice. Please enter 1, 2, 3, or 4."
            )
