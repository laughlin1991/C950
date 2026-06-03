class Package:

    def __init__(self, package_id, address, deadline, city, zip_code, weight, special_notes=""):

        self.package_id = package_id
        self.address = address
        self.deadline = deadline
        self.city = city
        self.zip_code = zip_code
        self.weight = weight
        self.special_notes = special_notes

        self.status = "at hub"
        self.delivery_time = None

    def __str__(self):

        output = "Package ID: " + str(self.package_id)
        output = output + " | Address: " + str(self.address)
        output = output + ", " + str(self.city)
        output = output + ", " + str(self.zip_code)
        output = output + " | Deadline: " + str(self.deadline)
        output = output + " | Weight: " + str(self.weight) + " kg"
        output = output + " | Status: " + str(self.status)
        output = output + " | Delivery Time: " + str(self.delivery_time)
        output = output + " | Notes: " + str(self.special_notes)
        return output
