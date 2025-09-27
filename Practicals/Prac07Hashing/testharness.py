from hashclasses import DSAHashTable
import os
import csv

def main():
    """
    Test harness to demonstrate DSAHashTable file I/O and resizing.
    Loads data from a CSV, forcing the table to grow, then removes data,
    forcing it to shrink.
    """
    input_filename = 'RandomNames7000.csv'
    output_filename = 'hash_table_contents_after_resize.csv'

    if not os.path.exists(input_filename):
        print(f"Error: Input file '{input_filename}' not found.")
        print("Please make sure the CSV file is in the same directory.")
        return

    # --- Phase 1: Load data and demonstrate table EXPANSION ---
    print("--- Phase 1: Loading data to trigger table expansion ---")
    
    # Start with a small capacity to ensure resizing happens multiple times
    name_table = DSAHashTable(101)
    print(f"Initial Table Capacity: {name_table.get_capacity()}")

    keys_in_table = []
    with open(input_filename, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        count = 0
        for row in reader:
            if len(row) == 2:
                user_id, name = row[0], row[1]
                name_table.put(name, user_id)
                keys_in_table.append(name) # Store keys for later removal
                count += 1

                # Print a status update every 500 entries
                if count % 500 == 0:
                    print(f"  Processed {count} entries. "
                          f"Load Factor: {name_table.get_load_factor():.2f} "
                          f"({name_table.get_count()}/{name_table.get_capacity()})")
    
    print("\n--- Hash Table Statistics After Loading ---")
    print(f"Total unique entries loaded: {name_table.get_count()}")
    print(f"Final table capacity after expansion: {name_table.get_capacity()}")
    print(f"Final load factor: {name_table.get_load_factor():.2f}")


    # --- Phase 2: Remove data and demonstrate table SHRINKING ---
    print("\n--- Phase 2: Removing data to trigger table shrinking ---")
    
    # Remove a large portion of the keys to trigger shrinking
    # The table will shrink when the load factor drops below 0.25
    items_to_remove_count = int(len(keys_in_table) * 0.85)
    print(f"Preparing to remove {items_to_remove_count} entries...")

    for i in range(items_to_remove_count):
        key_to_remove = keys_in_table[i]
        try:
            name_table.remove(key_to_remove)
        except KeyError:
            # This can happen if the key was a duplicate and already overwritten
            pass 
        
        # Print a status update every 500 removals
        if (i + 1) % 500 == 0:
            print(f"  Removed {i+1} entries. "
                  f"Load Factor: {name_table.get_load_factor():.2f} "
                  f"({name_table.get_count()}/{name_table.get_capacity()})")

    print("\n--- Hash Table Statistics After Removing ---")
    print(f"Entries remaining: {name_table.get_count()}")
    print(f"Final table capacity after shrinking: {name_table.get_capacity()}")
    print(f"Final load factor: {name_table.get_load_factor():.2f}")

    # --- Phase 3: Save the remaining hash table contents ---
    print("\n--- Phase 3: Saving remaining data to a new CSV ---")
    name_table.save_to_csv(output_filename)

    print(f"\nProcess complete. You can now inspect '{output_filename}'.")

if __name__ == "__main__":
    main()

