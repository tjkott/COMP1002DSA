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
        postfix_queue = self._parseInfixToPostfix(equation)
        result = self.evaluatePostfix(postfix_queue)
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


    def _get_precedence(self, operator):
        """Returns the precedence of the given operator."""
        if operator in ['+', '-']:
            return 1
        elif operator in ['*', '/']:
            return 2
        return 0
