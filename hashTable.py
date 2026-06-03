class HashTable:

#Initializes hash table with empty buckets
    def __init__(self, size=40):
        self.buckets = [[] for _ in range(size)]

#Computes the bucket index for a given key
    def _hash(self, key):
        return key % len(self.buckets)

#Insert/update a package using the package ID as the key
    def insert(self, key, package):
        bucket = self.buckets[self._hash(key)]
        for i in range(len(bucket)):
            if bucket[i][0] == key:
                bucket[i] = (key, package)
                return
        bucket.append((key, package))

#Returns a package using the package ID as they key
    def lookup(self, key):
        for pair in self.buckets[self._hash(key)]:
            if pair[0] == key:
                return pair[1]
        return None

#Return all packages
    def get_all_packages(self):
        all_packages = []
        for bucket in self.buckets:
            for pair in bucket:
                all_packages.append(pair[1])
        return all_packages
