class InvalidInputError(Exception):
    """Custome expetion written by me that is raised for errors in the input to functions."""
    pass

def calcNFactorialIterative(n):
    """Calculates the factorial of n iteratively."""
    # Exceptions
    if not isinstance(n, int):
        raise InvalidInputError("Input must be an integer!!!")
    if n < 0:
        raise InvalidInputError("Factorial is not defined for negative numbers")
    
    nfactorial = 1
    for ii in range(n, 1, -1):
        nFactorial = nFactorial * ii
    return nfactorial

def calcNFactorialRecursive(n):
    """Calculates the factorial of n recursively."""
    # Exceptions
    if not isinstance(n, int):
        raise InvalidInputError("Input must be an integer!!!")
    if n < 0:
        raise InvalidInputError("Factorial is not defined for negative numbers")
    # Base case and recursive case
    if (n < 0): # Check for negative input
        raise ValueError("Factorial is not defined for negative numbers")
    elif (n == 0): # Base case for recursion
        factorial = 1
    else:
        factorial = n * calcNFactorialRecursive(n - 1) # function itself is called again.
    return factorial 
print(calcNFactorialRecursive(5)) # Example usage

def fibIterative(n):
    """Calculates the nth Fibonacci number iteratively."""
    if not isinstance(n, int):
        raise InvalidInputError("Input must be an integer!!!")
    if n < 0:
        raise InvalidInputError("Fibonacci is not defined for negative numbers")

    if n <= 1:
        return
    
    lastVal, currVal = 0, 1
    for _ in range(2, n + 1):
        fibVal = currVal + lastVal
        lastVal = currVal
        currVal = fibVal
    return currVal

def fibRecursive(n):
    if not isinstance(n, int):
        raise InvalidInputError("Input must be an integer.!!   ")
    if n < 0:
        raise InvalidInputError("Fibonacci is not defined for negative numbers.")
    
    fibVal = 0

    if n == 0: # Base case for recursion
        fibVal = 0
    elif n == 1: # Base case for recursion
        fibVal = 1
    else:
        fibVal = fibRecursive(n - 1) + fibRecursive(n - 2) # function itself is called again.
    return fibVal

def gcdRecursive(a, b):
    if not isinstance(a, int) or not isinstance(b, int):
        raise InvalidInputError("Inputs must be integers.")
    """Calculates the GCD of a and b recursively."""
    if b == 0:
        return a
    else:
        return gcdRecursive(b, a % b)

def convertToBase_recursive(n, base):
    """Converts a number n to a given base recursively."""
    
    if not isinstance(n, int) or not isinstance(base, int):
        raise InvalidInputError("Inputs must be integers.")
    if n< 0:
        raise InvalidInputError("Number must be non-negative.")
    if base < 2 or base > 16:
        raise InvalidInputError("Base must be between 2 and 16.")
    
    conversion_characters = "0123456789ABCDEF"
    
    if n < base:
        #  base case: when number < base, it's a single digit. Stop the recursion and return character. 
        return conversion_characters[n] 
    else:
        # recursive case: if number is larger than the base:
        # 1. Make a recursive call with the number divided by the base n // base
        # 2. Get the remainder of the current number and append the character for the remainder. 
        return convertToBase_recursive(n // base, base) + conversion_characters[n % base]

