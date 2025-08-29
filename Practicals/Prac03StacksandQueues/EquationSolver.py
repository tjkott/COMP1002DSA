# Author: Thejana Kottawatta Hewage (22307822)
# Data Structures and Algorithms COMP1002
# 
# EquationSolver.py - COnverts infix form to postfix then evaluates the postfix. 
#

from classes import DSAStack, DSACircularQueue

class EquationSolver:
    """
    Class to solve equations in infix notation.
    """
    def solve(self, equation):
        postfixQueue = self._parseInfixToPostfix(equation)
        result = self._evaluatePostfix(postfixQueue) # calls private helper method to calculate the final answer from the postfix queue. 
        return result
    
    def _parseInfixToPostfix(self, equation):
        """Converts infix equation to postfix equation."""

        postfixQueue = DSACircularQueue()
        opStack = DSAStack() # Stack for operators
        tokens = equation.split(" ") # Split the equation into tokens at spaces

        for term in tokens:
            if term == '(': 
                opStack.push(term) # '(' Gets put straight onto the stack. 
            elif term == ')':
                while not opStack.isEmpty() and opStack.top() != '(': # Find corresponding '('
                    postfixQueue.enqueue(opStack.pop()) # pop remaining operaors for the bracketed sub-equation
                if opStack.isEmpty():
                    raise ValueError("Mismatched parentheses in equation.")
                opStack.pop() # pop the '(' and discard it.
            elif term in ['+', '-', '*', '/']:
                while (not opStack.isEmpty() and 
                       opStack.top() != '(' and
                       self._get_precedence(opStack.top()) >= self._get_precedence(term)):
                    postfixQueue.enqueue(opStack.pop()) # Move higher/equal precedence ops to postfix eqn
                opStack.push(term) # put the new operator on to the stack.
            else: # else term is an operand.
                postfixQueue.enqueue(float(term)) # add operand to the postfix equation.

        while not opStack.isEmpty(): # pop any remaining operators from the stack. 
            if opStack.top() == '(':
                raise ValueError("Mismatched parentheses in equation.")
            postfixQueue.enqueue(opStack.pop())

        return postfixQueue
    
    def _evaluatePostfix(self, postfixQueue):
        """Take the postfix queue and evaluates it."""
        opStack = DSAStack()
        while not postfixQueue.isEmpty():
            term = postfixQueue.dequeue()
            if isinstance(term, float):
                opStack.push(term)
            else: # else it should be an operator. 
                op2 = opStack.pop()
                op1 = opStack.pop()
                result = self._execute_operation(term, op1, op2)
                opStack.push(result)
        if opStack.get_count() != 1:
            raise ValueError("Invalid postfix equation.")
        return opStack.pop()

    def _get_precedence(self, operator):
        """Returns the precedence of the given operator."""
        if operator in ['+', '-']:
            return 1
        elif operator in ['*', '/']:
            return 2
        return 0
    
    def _execute_operation(self, op, op1, op2):
        if op == '+':
            return op1 + op2
        elif op == '-':
            return op1 - op2
        elif op == '*':
            return op1 * op2
        elif op == '/':
            if op2 == 0:
                raise ValueError("Division by zero.")
            return op1 / op2


if __name__ == '__main__':
    solver = EquationSolver()
    
    # List of test equations
    test_equations = ["3 * 4 + 5", #simple equation
        "( 3 + 4 ) * 5", # brackets
        "( 10.3 * ( 14 + 3.2 ) ) / ( 5 + 2 - 4 * 3 )"
    ]
    
    # Loop through the equations and solve them
    for i, eq in enumerate(test_equations):
        print(f"Equation {i+1}")
        print(f"Solving Infix: '{eq}'")
        
        try: # exceptions handling.
            # Step 1: Convert to postfix
            postfixEq = solver._parseInfixToPostfix(eq)
            print(f"Postfix version: {postfixEq}")
            
            # Step 2: Evaluate the postfix queue
            result = solver._evaluatePostfix(postfixEq)
            print(f"Result: {result}\n")
        except ValueError as e:
            print(f"Error solving equation: {e}\n")