# Author: Thejana Kottawatta Hewage (22307822)
# Data Structures and Algorithms COMP1002
# 
# Python file to hold all sorting methods
#

# Custom exceptions handling. 
class InvalidInputError(Exception):
    pass

def moveDisk(diskID, src, dest, level, moveID):
    """
    Prints the move of a disk. Adds indenting to output to show the level of recursion. 

    Param:
    diskID: The number of discs. 
    src: The source peg
    dest: The destination peg
    level: The current level of recursion
    moveID: The ID of the move

    'level' means how deep  you are int eh chaon of function calls. 
    Level 0 = Initial call to function. 
    Level 1 = When function calls itself, another function call is inside. 
    """
    indent = "  " * level #deeper level of recursion results in more spaces
    print(f"{indent}Recursion Level={level+1}")
    print(f"{indent}Moving Disk {diskID} from Source {src} to Destination {dest}")
    print(f"{indent}n={moveID}, src={src}, dest={dest}\n")

def towers(n, src, dest):
    # wrapper function. 
    # Exceptions handling:
    if not all(isinstance(i, int) for i in [n, src, dest]): 
        # checks if n, src and dest are all integers. 
        raise InvalidInputError("All inputs must be integers.")
    if n < 1: # ensures number of discs inputted is a positive number. 
        raise InvalidInputError("Number of disks must be at least 1.")
    if not (1<= src <= 3 and 1 <= dest <= 3 and src != dest):
        # source and destination pegs are valid (between 1-3) and source peg is not the same as destination peg. 
        raise InvalidInputError("Pegs must be 1, 2 or 3, and source cannot be the destination.")

    # Nested function to avoid input validation running more than once.
    def hanoiAlgorithm(number_of_disks, source, destination, level):
        if number_of_disks == 1:
            # base case - stop the recursion if there's ony one disk. 
            # move directly from source to destination. 
            moveDisk(1, source, destination, level, 1)
        else:
            #recursive step
            temp = 6 - source - destination # subtract source and destination peg to find remaining peg. 

            #step 1:  Move all but bottom disk to temp peg. 
            hanoiAlgorithm(number_of_disks - 1, source, temp, level + 1)

            #step #2: move the largest bottom disk from source to destination. 
            moveDisk(number_of_disks, source, destination, level, number_of_disks)

            #step #3L: move the rest from temp peg to on top of largest destination peg. . 
            hanoiAlgorithm(number_of_disks - 1, temp, destination, level + 1)

    hanoiAlgorithm(n, src, dest, 0)  # Start the recursive algorithm with level 0

if __name__ == "__main__":
    try:
        number_of_disks = int(input("Enter the number of disks (1-3): "))
        source_peg = 1
        destination_peg = 3

        towers(number_of_disks, source_peg, destination_peg)
    
    # exceptions handling. 
    except InvalidInputError as error:
        print(f"Invalid input: {error}")
    except ValueError: # Catching ValueError for invalid integer input
        print("Please enter a valid integer for the number of disks. (1 -3)")

