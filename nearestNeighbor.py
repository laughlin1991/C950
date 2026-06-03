from distanceTableLoader import get_location_index

def compute_routes(trucks, locations, distance_matrix):

    for truck in trucks:

        #Creates a stop for each address location
        stops = []
        for package in truck.packages:
            index = get_location_index(package.address, locations)
            if index not in stops:
                stops.append(index)

        #Starts at the hub
        route = [0]
        current = 0

        #Chooses the nearest location from the remaining stops
        while len(stops) > 0:
            nearest = min(stops, key=lambda i: distance_matrix[current][i])
            route.append(nearest)
            current = nearest
            stops.remove(nearest)

        # Return to hub
        route.append(0)
        truck.route = route
