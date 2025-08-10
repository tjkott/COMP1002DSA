class InvalidInputError(Exception):
    pass

def moveDisk(diskID, src, dest, level, moveID):
    """
    Prints the move of a disk. Adds indenting to output to show the level of recursion. 

    Param:
    diskID: The ID of the disk to move
    src: The source peg
    dest: The destination peg
    level: The current level of recursion
    moveID: The ID of the move
    """
    indent = "  "*level
    print(f"{indent}Recursion Level={level+1}")
    print(f"{indent}Moving Disk {diskID} from Source {src} to Destination {dest}")
    print(f"{indent}n={moveID}, src={src}, dest={dest}\n")

def towers(n, src, dest):
    # Exceptions:
    if not all(isinstance(i, int) for i in [n, src, dest]):
        raise InvalidInputError("All inputs must be integers.")
    if n < 1:
        raise InvalidInputError("Number of disks must be at least 1.")
    if not (1<= src <= 3 and 1 <= dest <= 3 and src != dest):
        raise InvalidInputError("Pegs must be 1, 2 or 3, and source cannot be the destination.")

    # Nested function to avoid input validation running > once.
    def hanoiAlgorithm(number_of_disks, source, destination, level):
        if number_of_disks == 1:
            moveDisk(1, source, destination, level, 1)
        else:
            tmp = 6 - source - destination
            # Move all but bottom disk to temp peg. 
            hanoiAlgorithm(number_of_disks - 1, source, tmp, level + 1)
            # Move bottom disk to target peg destination. 
            moveDisk(number_of_disks, source, destination, level, number_of_disks)
            # move the rest from temp peg to target peg detination. 
            hanoiAlgorithm(number_of_disks - 1, tmp, destination, level + 1)

    hanoiAlgorithm(n, src, dest, 0)  # Start the recursive algorithm with level 0

if __name__ == "__main__":
    try:
        number_of_disks = int(input("Enter the number of disks (1-3): "))
        source_peg = 1
        destination_peg = 3

        towers(number_of_disks, source_peg, destination_peg)
    
    except InvalidInputError as error:
        print(f"Invalid input: {error}")
    except ValueError: # Catching ValueError for invalid integer input
        print("Please enter a valid integer for the number of disks.")