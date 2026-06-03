import csv

#Loads location names and a distance matrix from the CSV file
def load_distances(file_path):

    locations = []
    distance_matrix = []

    with open(file_path, newline="", encoding="utf-8-sig") as csv_file:
        for row in csv.reader(csv_file):
            if len(row) > 1 and row[1].strip() != "" and row[0].strip() != "":
                locations.append(row[1].strip())
                values = [float(x) if x.strip() != "" else 0.0 for x in row[2:]]
                distance_matrix.append(values)

    for i in range(len(distance_matrix)):
        while len(distance_matrix[i]) < len(locations):
            distance_matrix[i].append(0.0)
        for j in range(i + 1, len(locations)):
            distance_matrix[i][j] = distance_matrix[j][i]

    return (locations, distance_matrix)

#Returns the index of a location that matches the given string
def get_location_index(address, locations):

    address_lower = address.lower()

    for location_index in range(len(locations)):
        current_location = locations[location_index]
        current_location_lower = current_location.lower()
        if address_lower in current_location_lower:
            return location_index

    return 0
