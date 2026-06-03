import csv
from packageClass import Package

#Reads each package from the CSV file and inserts them into the hash table
def load_packages(file_path, hash_table):
    with open(file_path, newline="", encoding="utf-8-sig") as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        for row in reader:
            if len(row) == 0:
                continue
            try:
                package_id = int(row[0].strip())
            except ValueError:
                continue

            deadline = row[5].strip() if len(row) > 5 and row[5].strip() != "" else "EOD"

            weight = row[6].strip() if len(row) > 6 and row[6].strip() != "" else "0"

            special_notes = row[7].strip() if len(row) > 7 and row[7].strip() != "" else ""

            hash_table.insert(package_id, Package(
                package_id,
                row[1].strip(),
                deadline,
                row[2].strip(),
                row[4].strip(),
                weight,
                special_notes
            ))

