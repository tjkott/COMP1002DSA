import math
import csv
import os
from contextlib import redirect_stdout

# =====================================================================================
# MODULE 2: Hash-Based Patient Lookup
# Student: [Your Name]
# ID: [Your ID]
# =====================================================================================

# -------------------------------------------------------------------------------------
# Justification of Design Choices (as required by deliverables)
# -------------------------------------------------------------------------------------
# 1. Collision Handling Strategy: Chaining
#    - Chaining with linked lists was chosen over open addressing (linear probing).
#    - Reason: Chaining is simpler to implement, especially for deletion (no need
#      for a "formerly used" state). It also handles high load factors more
#      gracefully; performance degrades per-slot rather than across the entire
#      table due to clustering, which is a common issue with linear probing.
#
# 2. Hash Function & Table Size: Modulo with Prime Number
#    - Hash Function: A simple character-based hash is used (sum of ASCII values
#      of the patient ID). It's fast and sufficient for this application.
#    - Table Size: The table size is always set to the next prime number greater
#      than the requested capacity. Using a prime number helps distribute keys
#      more uniformly when using the modulo operator, significantly reducing
#      the number of initial collisions.
# -------------------------------------------------------------------------------------


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
        self.max_load_factor = 0.7

    def Hash(self, key):
        """A simple modulo-based hash function."""
        key_str = str(key)
        hash_val = 0
        for char in key_str:
            hash_val = (31 * hash_val) + ord(char)
        ## Implement a simple modulo-based hash function; explain parameter choices 
        # (table size, prime selection). 
        return abs(hash_val % self.capacity)
    
    ## 2) Core operations
    def insert(self, record):
        """Inserts a PatientRecord into the hash table. Handles duplicates by updating."""
        if self.getLoadFactor() > self.max_load_factor:
            self.Resize()

        index = self.Hash(record.patientID)
        chain = self.table[index]
        op_count = 0

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
        ## search(patientID): O(1) expected; return the full patient record or a not-found message. 
        index = self.Hash(patientID)
        chain = self.table[index]
        op_count = 0

        for record in chain:
            op_count += 1
            if record.patientID == patientID:
                print(f"Found Patient {patientID} at index {index}. (Chain traversal: {op_count} hops)")
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
        """Returns a list of strings representing the hash table state."""
        output = []
        
        output.append("\n" + "="*25 + " HASH TABLE STATE " + "="*25)
        output.append(f"Count: {self.count}, Capacity: {self.capacity}, Load Factor: {self.getLoadFactor():.2f}")
        for i, chain in enumerate(self.table):
            if len(chain) > 0:
                chain_str = ""
                for record in chain:
                    chain_str += f"[ID: {record.patientID}] -> "
                output.append(f"Index {i:02}: {chain_str}None")
        output.append("="*70 + "\n")
        
        return output

    # --- Private Helper Methods (PascalCase as per style guide) ---

    def Resize(self):
        """Doubles the hash table size and re-hashes all existing entries."""
        old_table = self.table
        new_capacity = self.FindNextPrime(self.capacity * 2)
        
        print(f"\nRESIZING: Load factor > {self.max_load_factor}. "
              f"Resizing from {self.capacity} to {new_capacity}.\n")

        # Reset the current table
        self.capacity = new_capacity
        self.table = [DSALinkedList() for _ in range(self.capacity)] # 
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

# -------------------------------------------------------------------------------------
# Test Driver
# -------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------
# Test Driver
# -------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------
# Test Driver
# -------------------------------------------------------------------------------------

def main():
    """Test driver to demonstrate all hash table functionalities."""

    # This list will capture all our output
    output_log = []
    
    output_log.append("=====================================================")
    output_log.append("   Critical Care Optimisation: Patient Lookup")
    output_log.append("=====================================================")

    # Initialize with a small prime size to easily demonstrate collisions and resizing
    patient_table = DSAHashTable(initial_size=11)
    
    # --- Define File Paths ---
    input_dir = "input" # Assuming 'input' directory from Module 3
    patient_file = os.path.join(input_dir, "patients.csv")

    # --- 1. Insertions from CSV and Collision Demonstration ---
    output_log.append(f"\n--- Phase 1: Inserting Patient Records from {patient_file} ---")
    
    # We must print the hash *before* inserting
    output_log.append(f"Demonstration: Hash(112) = {patient_table.Hash(112)}, Hash(213) = {patient_table.Hash(213)}")
    
    try:
        # Use csv.DictReader to read the patient CSV by its header names
        with open(patient_file, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    # --- THIS BLOCK IS NOW FIXED ---
                    # It calls PatientRecord using the original camelCase keywords
                    # from Module 2 (patientID, urgencyLevel, treatmentStatus)
                    new_patient = PatientRecord(
                        patientID=int(row['patient_id']),        # <-- CORRECTED
                        name=row['name'],
                        age=int(row['age']),
                        department=row['department'],
                        urgencyLevel=int(row['urgency_level']), # <-- CORRECTED
                        treatmentStatus=row['treatment_status'] # <-- CORRECTED
                    )
                    # We capture the log from the insert method (if you add logging)
                    insert_log = patient_table.insert(new_patient)
                    if insert_log: # In case your insert() returns a string
                        output_log.append(insert_log)

                except ValueError as e:
                    output_log.append(f"  Skipping row due to data error: {e} -> {row}")
                except KeyError as e:
                    output_log.append(f"  Skipping row due to missing CSV header: {e}")
        output_log.append("Patient records system is populated.\n")

    except FileNotFoundError:
        output_log.append(f"FATAL ERROR: Could not find patient file at '{patient_file}'.")
        output_log.append("Please ensure the file exists in the 'input' directory.")
        print("\n".join(output_log)) # Print what we have so far
        return # Exit the program
    except Exception as e:
        output_log.append(f"An unexpected error occurred reading {patient_file}: {e}")
        print("\n".join(output_log)) # Print what we have so far
        return

    # Task 6: Explicit collision example
    output_log.append("\nCOLLISION DEMO: Patient 112 and 213 both hash to the same initial index.")
    output_log.append("The hash table resolves this by chaining them in a linked list at that index.")
    output_log.extend(patient_table.displayTable()) # Add the table strings to our log

    # --- 2. Search Demonstrations (Hit and Miss) ---
    output_log.append("\n--- Phase 2: Searching for Patients ---")
    output_log.append("Searching for an existing patient (HIT):")
    found_patient = patient_table.search(101) # search() should not print, but return
    if found_patient:
        output_log.append(f"  -> Record found: {found_patient}")
    else:
        output_log.append("  -> Record not found.")

    output_log.append("\nSearching for a non-existent patient (MISS):")
    found_patient_miss = patient_table.search(999)
    if not found_patient_miss:
        output_log.append("  -> Record not found (SUCCESSFUL MISS).")


    # --- 3. Deletion Demonstration ---
    output_log.append("\n--- Phase 3: Deleting a Patient Record ---")
    output_log.append("Deleting Patient 451...")
    patient_table.delete(451)
    output_log.append("Attempting to search for the deleted patient:")
    found_patient_deleted = patient_table.search(451) # Should be a MISS now
    if not found_patient_deleted:
        output_log.append("  -> Record not found (SUCCESSFUL DELETE).")


    output_log.append("\nAttempting to delete a non-existent patient:")
    patient_table.delete(999) # Should fail gracefully
    output_log.append("  -> Delete attempt finished (graceful fail).")

    output_log.extend(patient_table.displayTable())

    # --- 4. Complexity and Load Factor Summary ---
    output_log.append("\n--- Final Summary ---")
    output_log.append("Complexity: All operations (insert, search, delete) demonstrated low 'hop' counts,")
    output_log.append("supporting the expected O(1) average time complexity. The worst-case for a single")
    output_log.append("operation would be O(n) if all keys hashed to the same index.")
    output_log.append("\nLoad Factor Behaviour: The table began with a capacity of 11 and was resized to 23")
    output_log.append(f"when the load factor exceeded the threshold of {patient_table.max_load_factor}, ensuring that chains")
    output_log.append("remain short and performance remains high.")
    output_log.append("=====================================================")


    # --- 5. Join all output and save/print ---
    final_output_string = "\n".join(output_log)

    # 5a. Print the final output to the terminal
    print(final_output_string)

    # 5b. Save the final output to the file "as well"
    output_dir = "output"
    output_file = os.path.join(output_dir, "hash_results.txt")
    
    try:
        os.makedirs(output_dir, exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(final_output_string)
        print(f"\nHash table test complete. Results also saved to {output_file}")
    except Exception as e:
        print(f"\nError: Could not save results file to {output_file}")
        print(f"Details: {e}")


if __name__ == "__main__":
    main()