# MODULE 3: Hash-Based Patient Lookup
# Author: Thejana Kottawatta (22307822)

import math
import sys
import csv
import os
from contextlib import redirect_stdout

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

    def removeByPatientId(self, patient_id):
        """Removes a record from the list based on patient_id. Returns the removed record or None."""
        prev, current = None, self.head
        while current is not None:
            if current.value.patient_id == patient_id:
                if prev is None:
                    self.head = current.next
                else:
                    prev.next = current.next
                self.count -= 1
                return current.value
            prev, current = current, current.next
        return None

    def __iter__(self):
        current = self.head
        while current:
            yield current.value
            current = current.next

    def __len__(self):
        return self.count

class PatientRecord:
    """A simple class to structure patient data."""
    def __init__(self, patient_id, name, age, department, UrgencyLevel, TreatmentStatus="Admitted"):
        # Task 4 (Module 2): Input Validation
        if not isinstance(patient_id, int) or patient_id <= 0:
            raise ValueError("PatientID must be a positive integer.")
        if not name or not isinstance(name, str):
            raise ValueError("Name cannot be empty and must be a string.")
        if not isinstance(UrgencyLevel, int) or not (1 <= UrgencyLevel <= 5):
            raise ValueError("Urgency Level must be an integer between 1 and 5.")

        self.patient_id = patient_id
        self.name = name
        self.age = age
        self.department = department
        self.urgency_level = UrgencyLevel
        self.treatment_status = TreatmentStatus

    def __str__(self):
        """Provides a clean, readable string representation of the patient record."""
        return (f"ID: {self.patient_id}, Name: {self.name}, Age: {self.age}, "
                f"Dept: {self.department}, Urgency: {self.urgency_level}, "
                f"Status: {self.treatment_status}")

class DSAHashTable:
    """A hash table implementation using chaining with DSALinkedList for collision resolution."""

    def __init__(self, initial_size=23):
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
        return abs(hash_val % self.capacity)

    def insert(self, record):
        """Inserts a PatientRecord into the hash table. Handles duplicates by updating."""
        if self.getLoadFactor() > self.max_load_factor:
            self.Resize()

        index = self.Hash(record.patient_id)
        chain = self.table[index]

        for existing_record in chain:
            if existing_record.patient_id == record.patient_id:
                existing_record.name = record.name
                existing_record.age = record.age
                existing_record.department = record.department
                existing_record.urgency_level = record.urgency_level
                existing_record.treatment_status = record.treatment_status
                # print(f"UPDATE: Patient {record.patient_id} updated.")
                return

        chain.insertLast(record)
        self.count += 1


    def search(self, patient_id):
        """Searches for a patient by their ID and returns the full record."""
        index = self.Hash(patient_id)
        chain = self.table[index]

        for record in chain:
            if record.patient_id == patient_id:
                # print(f"SEARCH HIT: Found Patient {patient_id} at index {index}.")
                return record
        
        # print(f"SEARCH MISS: Patient {patient_id} not found.")
        return None

    def delete(self, patient_id):
        """Deletes a patient record by their ID."""
        index = self.Hash(patient_id)
        chain = self.table[index]
        removed_record = chain.removeByPatientId(patient_id)

        if removed_record:
            self.count -= 1
            # print(f"DELETE: Successfully removed Patient {patient_id}.")
        else:
            # print(f"DELETE FAIL: Patient {patient_id} not found.")
            pass

    def getLoadFactor(self):
        """Calculates the current load factor of the hash table."""
        return self.count / self.capacity

    # private methods

    def Resize(self):
        """Doubles the hash table size and re-hashes all existing entries."""
        old_table = self.table
        new_capacity = self.FindNextPrime(self.capacity * 2)
        
        print(f"\nRESIZING HASH TABLE: Load factor > {self.max_load_factor}. "
              f"Resizing from {self.capacity} to {new_capacity}.\n")

        self.capacity = new_capacity
        self.table = [DSALinkedList() for _ in range(self.capacity)]
        self.count = 0

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

class PriorityRequest:
    """A data structure to hold a scheduling request and its computed priority."""
    def __init__(self, patient_id, treatment_time, priority_score, patient_name, patient_urgency):
        self.patient_id = patient_id
        self.treatment_time = treatment_time
        self.priority_score = priority_score
        self.patient_name = patient_name
        self.patient_urgency = patient_urgency

    def __str__(self):
        """String representation for logging."""
        return (f"[ID: {self.patient_id} ({self.patient_name}), "
                f"Priority: {self.priority_score:.2f}, "
                f"U: {self.patient_urgency}, T: {self.treatment_time}m]")

class DSAEmergencyHeap:
    """
    An array-based Max Heap to schedule priority requests.
    Each slip will have 2 pieces of info: ID, and T. 
    """
    
    def __init__(self, max_size=100):
        """Initialise the heap with a fixed maximum size."""
        self.heap_array = [None] * max_size
        self.count = 0
    
    ## Implement: insert(request), peek(), extract_priority().
    def insert(self, patient_id, treatment_time, patient_table):
        """
        - Inserts a new request into the heap.
        - Fetches patient data from the hash table and computes priority.
        """
        # Task 3: Edge Case Handling
        ## Each request references a PatientID; retrieve UrgencyLevel and TreatmentStatus from the hash table. 
        record = patient_table.search(patient_id) # "Calling the recors office"
        
        # exceptions handling
        ## Handle invalid PatientID, zero/negative treatment time, or inactive status gracefully.
        if record is None:
            print(f"INSERT FAILED: Patient {patient_id} not found in records.")
            return
        if record.treatment_status != "Admitted":
            print(f"INSERT FAILED: Patient {patient_id} is not 'Admitted' (Status: {record.treatment_status}).")
            return
        if not isinstance(treatment_time, (int, float)) or treatment_time <= 0:
            print(f"INSERT FAILED: Invalid treatment time ({treatment_time}) for Patient {patient_id}.")
            return
        if self.count >= len(self.heap_array):
            print(f"INSERT FAILED: Heap is full. Cannot add Patient {patient_id}.")
            return

        U = record.urgency_level 

        ##  Use T (expected time) provided by scenario or by shortest-path estimates from Module 1 where applicable. 
        T = treatment_time 
        
        ## Compute the numeric priority for every request inserted.
        priority_score = (6 - U) + (1000 / T) # Priority = (6 - U) + 1000 / T
        
        new_request = PriorityRequest(patient_id, T, priority_score, record.name, U)
        
        # Task 4: Log priority computation
        print(f"INSERTING: {new_request.patient_name} (ID: {patient_id}) with U={U}, T={T}m. "
              f"Priority = (6-{U}) + (1000/{T}) = {priority_score:.2f}")

        self.heap_array[self.count] = new_request # inititially insert at the bery end of the line. 
        # New insert might be more important than its parent. 
        self.TrickleUp(self.count) ## Maintain heap invariants after each operation (percolate up/down). 
        self.count += 1
        
        self.displayHeapArray() ## Print the heap array after each insert and each extract_priority. 

    def peek(self):
        """Peek which entry is the highest priority"""
        if self.count == 0:
            return None
        return self.heap_array[0] # return root element without removing (i.e. peeking)

    def extract_priority(self):
        """Returns the highest priority request from the heap."""
        if self.count == 0: # exceptions handling
            print("EXTRACT FAILED: Heap is empty.")
            return None
        
        priority_request = self.heap_array[0] # pull the highest priority request (root)
        
        # In order to cause least amount of shuffling:
        # Decrement count and move the last element to the root
        self.count -= 1
        self.heap_array[0] = self.heap_array[self.count]
        self.heap_array[self.count] = None # Clear the last element's spot

        # Now have least prioritised element in most important. 
        # Restore the heap by trickling down from the root
        self.TrickleDown(0) ## percolate down

        # Task 4: Log extraction and print heap state
        print(f"EXTRACTED: {priority_request}")
        self.displayHeapArray()
        return priority_request

    def displayHeapArray(self):
        """Task 4: Prints the current state of the heap array for tracing."""
        print("  Heap State: ", end="")
        if self.count == 0:
            print("[EMPTY]")
            print("-" * 70) # Separator
            return
        
        # Manually format the list output
        array_str = "["
        for i in range(self.count): # Loop from 0 to count-1
            array_str += f"(Idx {i}: ID {self.heap_array[i].patient_id}, Pri {self.heap_array[i].priority_score:.2f})"
            if i < self.count - 1:
                array_str += ", "
        array_str += "]"
        print(array_str)
        print("-" * 70) # Separator

    ## Private MEthods ##
    def TrickleUp(self, index):
        """Moves an element up the heap to maintain the max-heap property (0-based)."""
        parent_index = (index - 1) // 2
        
        # While not at root and child is greater than parent
        while index > 0 and self.heap_array[index].priority_score > self.heap_array[parent_index].priority_score:
            # Swap child and parent
            temp = self.heap_array[index]
            self.heap_array[index] = self.heap_array[parent_index]
            self.heap_array[parent_index] = temp
            
            # Move up
            index = parent_index
            parent_index = (index - 1) // 2

    def TrickleDown(self, index):
        """Moves an element down the heap to maintain the max-heap property (0-based)."""
        left_child_index = 2 * index + 1
        
        while left_child_index < self.count:
            # Find the index of the child with the maximum priority
            max_child_index = left_child_index
            right_child_index = left_child_index + 1
            
            if (right_child_index < self.count and 
                self.heap_array[right_child_index].priority_score > self.heap_array[max_child_index].priority_score):
                max_child_index = right_child_index

            # If parent is less than the max child, swap them
            if self.heap_array[index].priority_score < self.heap_array[max_child_index].priority_score:
                temp = self.heap_array[index]
                self.heap_array[index] = self.heap_array[max_child_index]
                self.heap_array[max_child_index] = temp
                
                # Move down
                index = max_child_index
                left_child_index = 2 * index + 1
            else:
                break


def main():
    # Output file
    output_dir = "output"
    output_file = os.path.join(output_dir, "3heap_results.txt")
    os.makedirs(output_dir, exist_ok=True) # Create the directory if it doesn't exist

    print(f"Output saved on: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        with redirect_stdout(f):
            print("===========================================================")
            print("###   Critical Care Optimisation: Emergency Scheduler   ###")
            print("===========================================================\n")

            input_dir = "input" # input directory
            patient_file = os.path.join(input_dir, "patients.csv")
            requests_file = os.path.join(input_dir, "requests.csv")
 
            print(f"### Step 1: Initisalising hash table to store Patient Records from {patient_file} ###", flush=True)
            patient_table = DSAHashTable(initial_size=23) # small prime number
            
            try:
                with open(patient_file, mode='r') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        try:
                            new_patient = PatientRecord(patient_id=int(row['patient_id']),
                                                        name=row['name'],
                                                        age=int(row['age']),
                                                        department=row['department'],
                                                        UrgencyLevel=int(row['urgency_level']),   
                                                        TreatmentStatus=row['treatment_status'])
                            patient_table.insert(new_patient)
                        except ValueError as e:
                            print(f"  Skipping row due to data error: {e} -> {row}", flush=True)
                        except KeyError as e:
                            print(f"  Skipping row due to missing CSV header: {e}", flush=True)
                print("Patient records system is populated.\n", flush=True)
        
            except FileNotFoundError:
                print(f"FATAL ERROR: Could not find patient file at '{patient_file}'.", flush=True)
                print("Please ensure the file exists in the 'input' directory.", flush=True)
                return # Exit the program
            except Exception as e:
                print(f"An unexpected error occurred reading {patient_file}: {e}", flush=True)
                return
        
            ## Demonstrate at least 10 inserts and 5 extractions in a reproducible test run.
            print(f"### Step 2: Inserting 10 Emergency Requests from {requests_file} ###", flush=True)
            scheduler = DSAEmergencyHeap(max_size=20)
            
            try:
                with open(requests_file, mode='r', encoding='utf-8') as file:
                    reader = csv.DictReader(file) # patient requests csv file
                    for row in reader:
                        try:
                            patient_id_int = int(row['patient_id'])
                            t_time = int(row['treatment_time'])
                            scheduler.insert(patient_id_int, t_time, patient_table)
                        except ValueError as e:
                            print(f"  Skipping request due to data error: {e} -> {row}", flush=True)
                        except KeyError as e:
                            print(f"  Skipping request due to missing CSV header: {e}", flush=True)
        
            except FileNotFoundError:
                print(f"FATAL ERROR: Could not find request file at '{requests_file}'.", flush=True)
                print("Please ensure the file exists in the 'input' directory.", flush=True)
                return # Exit the program
            except Exception as e:
                print(f"An unexpected error occurred reading {requests_file}: {e}", flush=True)
                return
        
            print("\n### Step 3: Edge Case ###", flush=True)
            scheduler.insert(patient_id=999, treatment_time=30, patient_table=patient_table)
            scheduler.insert(patient_id=101, treatment_time=0, patient_table=patient_table)
            
            # Patient not 'Admitted' (demonstrate by deleting them first)
            print("\n(Demo: Deleting patient No. 1010 from records...)", flush=True)
            patient_table.delete(1010) # 1010 was loaded from the CSV
            scheduler.insert(patient_id=1010, treatment_time=30, patient_table=patient_table)
            print("-" * 70, flush=True) 
        
            print("\n### Step 4: Extracting Top 5 Priority Patients ---", flush=True)
            print("Expected order: 112(103.0), 745(71.7), 304(55.0), 633(44.0), 101(37.3)", flush=True)
            print("-" * 70, flush=True) 
            
            for i in range(5):
                print(f"\nExtracting patient {i+1}...", flush=True)
                request = scheduler.extract_priority()
                if request is None:
                    print("Scheduler is empty, stopping extraction.", flush=True)
                    break
                    
            print("\n### Final Summary ###", flush=True)
            print("""Evidence: The extraction log clearly shows that patients with the highest computed 
                  priority scores (e.g., 103.0, 71.7) were extracted first, regardless of the order they 
                  were inserted in. This confirms the Max Heap function is serving higher-priority patients first consistently. """, flush=True)
    print(f"Module 4 complete running. Results saved to {output_file}")


if __name__ == "__main__":
    main()