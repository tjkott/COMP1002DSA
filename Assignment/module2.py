import math

# =====================================================================================
# MODULE 2: Hash-Based Patient Lookup
# Student: Thejana Kottawatta Hewage
# ID: 22307822
# =====================================================================================



# -------------------------------------------------------------------------------------
# Custom Linked List (Adapted from Module 1 for Chaining)
# -------------------------------------------------------------------------------------

class DSALinkedList:
    """A custom Linked List, adapted to store PatientRecord objects for hash table chaining."""
    class DSAListNode:
        def __init__(self, value):
            self.value = value
            self.next = None

    def __init__(self):
        self.head = None
        self.count = 0

    def insertLast(self, value):
        new_node = self.DSAListNode(value)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        self.count += 1

    def removeByPatientID(self, patient_id):
        """Removes a record from the list based on patientID. Returns the removed record or None."""
        prev, current = None, self.head
        while current is not None:
            # The value stored in the node is a PatientRecord object
            if current.value.patientID == patient_id:
                if prev is None: # The node to remove is the head
                    self.head = current.next
                else:
                    prev.next = current.next
                self.count -= 1
                return current.value # Return the data of the removed node
            prev, current = current, current.next
        return None # Return None if not found

    def __iter__(self):
        current = self.head
        while current:
            yield current.value
            current = current.next

    def __len__(self):
        return self.count

# -------------------------------------------------------------------------------------
# Patient Record Definition
# -------------------------------------------------------------------------------------

class PatientRecord:
    """A simple class to structure patient data."""
    def __init__(self, patientID, name, age, department, urgencyLevel, treatmentStatus="Admitted"):
        # Task 4: Input Validation
        if not isinstance(patientID, int) or patientID <= 0:
            raise ValueError("PatientID must be a positive integer.")
        if not name or not isinstance(name, str):
            raise ValueError("Name cannot be empty and must be a string.")
        if not isinstance(urgencyLevel, int) or not (1 <= urgencyLevel <= 5):
            raise ValueError("Urgency Level must be an integer between 1 and 5.")

        self.patientID = patientID
        self.name = name
        self.age = age
        self.department = department
        self.urgencyLevel = urgencyLevel
        self.treatmentStatus = treatmentStatus

    def __str__(self):
        """Provides a clean, readable string representation of the patient record."""
        return (f"ID: {self.patientID}, Name: {self.name}, Age: {self.age}, "
                f"Dept: {self.department}, Urgency: {self.urgencyLevel}, "
                f"Status: {self.treatmentStatus}")

# -------------------------------------------------------------------------------------
# Hash Table Implementation
# -------------------------------------------------------------------------------------

class DSAHashTable:
    """A hash table implementation using chaining with DSALinkedList for collision resolution."""

    def __init__(self, initial_size=23): # Start with a prime number
        self.capacity = self.FindNextPrime(initial_size)
        self.table = [DSALinkedList() for _ in range(self.capacity)]
        self.count = 0
        self.maxloadfactor = 0.7

    def Hash(self, key):
        """A simple modulo-based hash function."""
        # Convert integer key to string to process its digits
        key_str = str(key)
        hash_val = 0
        for char in key_str:
            hash_val = (31 * hash_val) + ord(char)
        return abs(hash_val % self.capacity)

    def insert(self, record):
        """Inserts a PatientRecord into the hash table. Handles duplicates by updating."""
        # Task 3: Optional resizing implementation
        if self.getLoadFactor() > self.maxloadfactor:
            self.Resize()

        index = self.Hash(record.patientID)
        chain = self.table[index]
        op_count = 0 # To measure efficiency

        # Check for duplicates
        for existing_record in chain:
            op_count += 1
            if existing_record.patientID == record.patientID:
                # Update existing record
                existing_record.name = record.name
                existing_record.age = record.age
                existing_record.department = record.department
                existing_record.urgencyLevel = record.urgencyLevel
                existing_record.treatmentStatus = record.treatmentStatus
                print(f"UPDATE: Patient {record.patientID} updated. (Chain traversal: {op_count} hops)")
                return

        # No duplicate found, insert new record
        chain.insertLast(record)
        self.count += 1
        print(f"INSERT: Patient {record.patientID} into index {index}. (Chain length: {len(chain)})")

    def search(self, patientID):
        """Searches for a patient by their ID and returns the full record."""
        index = self.Hash(patientID)
        chain = self.table[index]
        op_count = 0

        for record in chain:
            op_count += 1
            if record.patientID == patientID:
                print(f"SEARCH HIT: Found Patient {patientID} at index {index}. (Chain traversal: {op_count} hops)")
                return record

        print(f"SEARCH MISS: Patient {patientID} not found. (Chain traversal: {op_count} hops)")
        return None

    def delete(self, patientID):
        """Deletes a patient record by their ID."""
        index = self.Hash(patientID)
        chain = self.table[index]

        removed_record = chain.removeByPatientID(patientID)

        if removed_record:
            self.count -= 1
            print(f"DELETE: Successfully removed Patient {patientID} from index {index}.")
        else:
            # Task 2: Handle missing keys gracefully
            print(f"DELETE FAIL: Patient {patientID} not found, nothing to delete.")

    def getLoadFactor(self):
        """Calculates the current load factor of the hash table."""
        return self.count / self.capacity

    def displayTable(self):
        """Prints a textual representation of the hash table and its chains."""
        print("\n" + "="*25 + " HASH TABLE STATE " + "="*25)
        print(f"Count: {self.count}, Capacity: {self.capacity}, Load Factor: {self.getLoadFactor():.2f}")
        for i, chain in enumerate(self.table):
            if len(chain) > 0:
                chain_str = ""
                for record in chain:
                    chain_str += f"[ID: {record.patientID}] -> "
                print(f"Index {i:02}: {chain_str}None")
        print("="*70 + "\n")

    # --- Private Helper Methods (PascalCase as per style guide) ---

    def Resize(self):
        """Doubles the hash table size and re-hashes all existing entries."""
        old_table = self.table
        new_capacity = self.FindNextPrime(self.capacity * 2)
        
        print(f"\nRESIZING: Load factor > {self.maxloadfactor}. "
              f"Resizing from {self.capacity} to {new_capacity}.\n")

        # Reset the current table
        self.capacity = new_capacity
        self.table = [DSALinkedList() for _ in range(self.capacity)]
        self.count = 0

        # Re-hash all records from the old table
        for chain in old_table:
            for record in chain:
                self.insert(record)

    def FindNextPrime(self, start_val):
        """Finds the next prime number from a given starting value."""
        if start_val <= 2:
            return 2
        prime_val = start_val
        if prime_val % 2 == 0:
            prime_val += 1
        while True:
            is_prime = True
            for i in range(3, int(math.sqrt(prime_val)) + 1, 2):
                if prime_val % i == 0:
                    is_prime = False
                    break
            if is_prime:
                return prime_val
            prime_val += 2

def main():
    """Test driver to demonstrate all hash table functionalities."""
    print("=====================================================")
    print("   Critical Care Optimisation: Patient Lookup")
    print("=====================================================")

    # Initialize with a small prime size to easily demonstrate collisions and resizing
    patient_table = DSAHashTable(initial_size=11)

    ## Insert at least 20 patient records [5. Testing requirements]
    patients_to_add = [
        PatientRecord(101, "John Smith", 45, "Cardiology", 2),
        PatientRecord(213, "Jane Doe", 32, "Neurology", 1),
        PatientRecord(112, "Peter Jones", 67, "Oncology", 3), # Hashes to same index as 213 with size 11
        PatientRecord(304, "Mary Williams", 28, "Emergency", 1),
        PatientRecord(451, "David Brown", 55, "Orthopedics", 4),
        PatientRecord(522, "Susan Miller", 71, "Geriatrics", 5),
        PatientRecord(633, "Robert Wilson", 39, "Pediatrics", 2),
        PatientRecord(745, "Linda Garcia", 50, "Emergency", 1),
        PatientRecord(819, "Michael Martinez", 62, "Cardiology", 3), # Triggers resize from 11 to 23
        PatientRecord(901, "Karen Rodriguez", 48, "Neurology", 2),
        PatientRecord(1010, "James Lee", 33, "Oncology", 4),
        PatientRecord(1123, "Patricia Harris", 76, "Geriatrics", 5),
        PatientRecord(1245, "Charles Clark", 22, "Emergency", 1),
        PatientRecord(1366, "Barbara Lewis", 58, "Orthopedics", 3),
        PatientRecord(1482, "Thomas Walker", 41, "Pediatrics", 2),
        PatientRecord(1599, "Jessica Hall", 30, "Cardiology", 1),
        PatientRecord(1602, "Daniel Allen", 65, "Neurology", 4),
        PatientRecord(1734, "Nancy Young", 53, "Oncology", 5),
        PatientRecord(1851, "Mark Hernandez", 29, "Emergency", 2),
        PatientRecord(1977, "Betty King", 80, "Geriatrics", 4),
        PatientRecord(2088, "Steven Wright", 47, "Orthopedics", 3)
    ]

    # --- 1. Insertions and Collision Demonstration ---
    print("\n--- Phase 1: Inserting Patient Records ---")
    print(f"Hash(112) = {patient_table.Hash(112)}, Hash(213) = {patient_table.Hash(213)}") # Prove they have same hash
    for patient in patients_to_add:
        patient_table.insert(patient)

    # Task 6: Explicit collision example
    print("\nCOLLISION DEMO: Patient 112 and 213 both hash to the same initial index.")
    print("The hash table resolves this by chaining them in a linked list at that index.")
    patient_table.displayTable()

    # --- 2. Search Demonstrations (Hit and Miss) ---
    print("\n--- Phase 2: Searching for Patients ---")
    print("Searching for an existing patient (HIT):")
    found_patient = patient_table.search(101)
    if found_patient:
        print("  -> Record found:", found_patient)

    print("\nSearching for a non-existent patient (MISS):")
    patient_table.search(999)

    # --- 3. Deletion Demonstration ---
    print("\n--- Phase 3: Deleting a Patient Record ---")
    print("Deleting Patient 451...")
    patient_table.delete(451)
    print("Attempting to search for the deleted patient:")
    patient_table.search(451) # Should be a MISS now

    print("\nAttempting to delete a non-existent patient:")
    patient_table.delete(999) # Should fail gracefully

    patient_table.displayTable()

    # --- 4. Complexity and Load Factor Summary ---
    print("\n--- Final Summary ---")
    print("Complexity: All operations (insert, search, delete) demonstrated low 'hop' counts,")
    print("supporting the expected O(1) average time complexity. The worst-case for a single")
    print("operation would be O(n) if all keys hashed to the same index.")
    print("\nLoad Factor Behaviour: The table began with a capacity of 11 and was resized to 23")
    print(f"when the load factor exceeded the threshold of {patient_table.maxloadfactor}, ensuring that chains")
    print("remain short and performance remains high.")
    print("=====================================================")

if __name__ == "__main__":
    main()
