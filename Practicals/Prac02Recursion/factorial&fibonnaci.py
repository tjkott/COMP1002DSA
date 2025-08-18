# Author: Thejana Kottawatta Hewage (22307822)
# Data Structures and Algorithms COMP1002
# 
# 
#
import time

class InvalidInputError(Exception):
    """Custom exception written by me that is raised for errors in the input to functions."""
    pass

def calcNFactorialIterative(n):
    """Calculates the factorial of n iteratively."""
    # Exceptions
    if not isinstance(n, int): # raises custom error if input 'n' is not an integer/ 
        raise InvalidInputError("Input must be an integer!!!")
    if n < 0: # Factorial will not be defined for negative numbers. 
        raise InvalidInputError("Factorial is not defined for negative numbers")
    
    nfactorial = 1 #initialises variable to store result. 
    for i in range(n, 1, -1): # loop backwards by 1 down to 1. 
        nfactorial = nfactorial * i
    return nfactorial
print(calcNFactorialIterative(5)) 
#print(calcNFactorialIterative(-5)) 
#print(calcNFactorialIterative('string')) 
#print(calcNFactorialIterative(1000))
def calcNFactorialRecursive(n):
    """Calculates the factorial of n recursively."""
    # Exceptions handling
    if not isinstance(n, int): 
        raise InvalidInputError("Input must be an integer!!!")
    if n < 0:
        raise InvalidInputError("Factorial is not defined for negative numbers")
    if n > 960:
        raise InvalidInputError("Factorial is undefined for numbers larger than 960 due to recursion limit in Python.")
    
    # Base case and recursive case
    if (n == 0): # Base case for recursion
        factorial = 1
    else: # recursive step
        # function calls itself with a slightly smaller problem. 
        # Multiplies n with the result of factorial of n-1
        factorial = n * calcNFactorialRecursive(n - 1) # function itself is called again.
    return factorial 
print(calcNFactorialRecursive(5)) # Example usage
print(calcNFactorialRecursive(980))

def fibIterative(n):
    """Calculates the nth Fibonacci number iteratively."""
    # Exceptions handling
    if not isinstance(n, int):
        raise InvalidInputError("Input must be an integer!!!")
    if n < 0:
        raise InvalidInputError("Fibonacci is not defined for negative numbers")

    if n <= 1:
        return
    
    # Initialise first 2 value in the sequence to start the pattern. 
    lastVal = 0 # 0th fib number
    currentVal = 1 # 1st fib number

    for _ in range(2, n + 1): # loops from 2 up to input number 'n'. 
        fibVal = lastVal + currentVal # = 0 + 1
        lastVal = currentVal #
        currentVal = fibVal
    return currentVal
print(fibIterative(5)) 
print(fibIterative(-5)) 
print(fibIterative('string')) 
print(fibIterative(1000))
def fibRecursive(n):
    if not isinstance(n, int):
        raise InvalidInputError("Input must be an integer.!!   ")
    if n < 0:
        raise InvalidInputError("Fibonacci is not defined for negative numbers.")
    
    fibVal = 0

    if n == 0: # Base case #1
        fibVal = 0
    elif n == 1: # Base case #2
        fibVal = 1
    else: # recursive step
        fibVal = fibRecursive(n - 1) + fibRecursive(n - 2) # function itself is called again.
    return fibVal
print(fibRecursive(5)) 
print(fibRecursive(-5)) 
print(fibRecursive('string')) 
print(fibRecursive(1000))

def gcdIterative(a, b):
    """Calculates GCD of a and b iteratively."""
    if not isinstance(a, int) or not isinstance(b, int): # validates that both are ints. 
        raise InvalidInputError("Inputs must be integers.")
    
    while b != 0:
        #
        a = b
        b = a % b # remainder of the old 'a' is divided by old ''
print(gcdIterative(5)) 
print(gcdIterative(-5)) 
print(gcdIterative('string')) 
print(gcdIterative(1000))
def gcdRecursive(a, b):
    """Calculates the GCD of a and b recursively."""
    # Exceptions handing:
    if not isinstance(a, int) or not isinstance(b, int): # validates that both are ints. 
        raise InvalidInputError("Inputs must be integers.")
    
    if b == 0: # base case
        return a
    else: # recursive step
        # Calls itself with the 2nd number b and the
        # remainder of the division of a by b. 
        # reducing the number till base base is reached. 
        return gcdRecursive(b, a % b)
print(gcdRecursive(5)) 
print(gcdRecursive(-5)) 
print(gcdRecursive('string')) 
print(gcdRecursive(1000))
def convertToBase_recursive(n, base):
    """Converts a number n to a given base recursively."""
    """
    (1) converToBase_recursive(26, 16)
    (2) 26 // 16 = 1, 26 % 16 = 10
    conversion_character[26 % 16 = 10] = A
    (3) conversion_char(1, 16) but 1 < 16 so base case. 
    (4) conversion_char[1] = "1". 
    (5) returns 1 + result from first step appended 'A"
    return = 1A. 
    """

    # Exceptions handiling. 
    if not isinstance(n, int) or not isinstance(base, int):
        raise InvalidInputError("Inputs must be integers.")
    if n< 0:
        raise InvalidInputError("Number must be non-negative.")
    if base < 2 or base > 16:
        raise InvalidInputError("Base must be between 2 and 16.")
    
    # base > sing digits. 1- = A, 11 = B etc. 
    conversion_characters = "0123456789ABCDEF"
    
    if n < base:
        #  base case: if base > number, it's a single digit. Stop the recursion and return character. 
        return conversion_characters[n] 
    else:
        # recursive step: if number is larger than the base:
        # 1. Make a recursive call with the number divided by the base (n // base)
        # 2. Get the remainder of the current number and append the character for the remainder. 
        return convertToBase_recursive(n // base, base) + conversion_characters[n % base]
print(convertToBase_recursive(26, 16))

def convertToBase_iterative(n, base):
    """Converts a number n to a given base iteratively."""
    if not isinstance(n, int) or not isinstance(base, int):
        raise InvalidInputError("Inputs must be integers.")
    if n < 0:
        raise InvalidInputError("Number must be non-negative.")
    if base < 2 or base > 16:
        raise InvalidInputError("Base must be between 2 and 16.")
    if n == 0:
        return "0"
    conversion_characters = "0123456789ABCDEF"
    baseResult = ""
    while n > 0:
        remainder = n % base
        baseResult = conversion_characters[remainder] + baseResult
        n = n // base
    return baseResult

def performanceTest(func, numSims, *args):
    """
    Tests the performance of a function over a number of simulations.

    Args:
        func: The function to test.
        num_simulations: The number of times to run the function.
        *args: The arguments to pass to the function.

    Returns:
        The average execution time in seconds.
    """
    TimeTotal = 0
    for _ in range(numSims):
        startTime = time.perf_counter() # measurement of short durations. 
        func(*args)
        endTime = time.perf_counter()
        TimeTotal += (endTime - startTime)
    
    return TimeTotal / numSims

# --- Main Execution Block ---

def performanceTestMain():
    """
    Main function to run the performance comparisons and print the results.
    """
    # Number of times to run each function to get a stable average.

    NUM_SIMULATIONS = 100
    
    # A small number for Fibonacci is chosen because the recursive version is very slow.
    fibN = 10
    factorialN = 50 # A larger number for factorial, as it's much faster.
    gcd_a, gcd_b = 1071, 462 # Standard example numbers for GCD.

    print("--- Performance Comparison: Iterative vs. Recursive ---")
    print(f"Running {NUM_SIMULATIONS} simulations for each function...\n")

    # 1. Factorial Test
    print(f"--- Testing Factorial with n = {factorialN} ---")
    time_fact_iter = performanceTest(calcNFactorialIterative, NUM_SIMULATIONS, factorialN)
    time_fact_rec = performanceTest(calcNFactorialRecursive, NUM_SIMULATIONS, factorialN)
    print(f"Iterative Factorial: {time_fact_iter:.8f} seconds (average)")
    print(f"Recursive Factorial: {time_fact_rec:.8f} seconds (average)\n")

    # 2. Fibonacci Test
    print(f"--- Testing Fibonacci with n = {fibN} ---")
    time_fib_iter = performanceTest(fibIterative, NUM_SIMULATIONS, fibN)
    time_fib_rec = performanceTest(fibRecursive, NUM_SIMULATIONS, fibN)
    print(f"Iterative Fibonacci: {time_fib_iter:.8f} seconds (average)")
    print(f"Recursive Fibonacci: {time_fib_rec:.8f} seconds (average)\n")

    # 3. GCD Test
    print(f"--- Testing GCD with a = {gcd_a}, b = {gcd_b} ---")
    time_gcd_iter = performanceTest(gcdIterative, NUM_SIMULATIONS, gcd_a, gcd_b)
    time_gcd_rec = performanceTest(gcdRecursive, NUM_SIMULATIONS, gcd_a, gcd_b)
    print(f"Iterative GCD:       {time_gcd_iter:.8f} seconds (average)")
    print(f"Recursive GCD:       {time_gcd_rec:.8f} seconds (average)\n")

    print("--- Summary ---")
    print("Factorial & GCD: Performance is very similar. The overhead of recursive function calls is minimal for these algorithms.")
    print("Fibonacci: The iterative version is DRAMATICALLY faster. The recursive version recalculates the same values many times, leading to exponential time complexity.")

if __name__ == "__main__":
    performanceTestMain()