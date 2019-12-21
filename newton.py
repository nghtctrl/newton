"""Newton's Method Calculator
Created on Fall 2019
CS108 Project
@author: Jiho Kim (jk249)
"""
from sympy.parsing.sympy_parser import parse_expr
from sympy import Symbol, root, sqrt, cbrt, log, ln, exp, pi, cos, sin, tan, \
    sec, csc, cot, acos, asin, atan, asec, acsc, acot
from validate import validate


class Newton:
    """
    Newton class for the Newton's Method Calculator

    This class assumes that all the types of data passed onto this class are correct types of data
    """
    def __init__(self):
        """This constructor instantiates the Newton's Method Calculator"""
        self.x = Symbol("x")

    def derive(self, expression):
        """This function calculates the derivative of the entered function"""
        if validate(expression):
            try:
                f_prime = parse_expr(expression).diff(self.x)
                return f_prime
            except SyntaxError:
                raise ValueError("Sorry! You've entered an invalid function...")
        else:
            raise ValueError("Sorry! You've entered an invalid function...")

    def newton(self, expression, initial_guess, max_iterations):
        """This function approximates root the given f, using Newton's method and returns the result in a list"""
        if validate(expression):
            try:
                f = parse_expr(expression)
            except SyntaxError:
                raise ValueError("Sorry! You've entered an invalid function...")
            f_prime = f.diff(self.x)

            x0 = initial_guess
            itr = max_iterations

            k = 1
            xn = 0

            list_of_results = []

            # Run this loop for the defined number of max_iterations
            while k <= itr:
                val = xn
                xn = x0 - f.evalf(subs=({self.x: x0})) / f_prime.evalf(subs=({self.x: x0}))
                x0 = xn

                # Remove unnecessary tailing zeros (e.g. 10.00000 to 10)
                if "." in str(xn):
                    xn_str = str(xn).rstrip("0").rstrip(".")
                else:
                    xn_str = str(xn)

                # Break out of the loop, if xn remains the same
                if xn == val:
                    if xn_str == "0":
                        list_of_results.append(xn_str)
                    break

                # Increment k and keep running the loop if xn is not the same
                k += 1

                list_of_results.append(xn_str)

            return list_of_results

        else:
            raise ValueError("Sorry! You've entered an invalid function...")


if __name__ == "__main__":
    nt = Newton()

    # Test for the default class variable
    assert nt.x == Symbol("x")

    # Test for ValueError on invalid expression
    try:
        nt.newton("siin(x)", 10, 10)
        assert False
    except ValueError:
        assert True

    # Test for ValueError on invalid expression
    try:
        nt.newton("x***2", 10, 10)
        assert False
    except ValueError:
        assert True

    # Test for ValueError on invalid expression
    try:
        nt.newton("x%50", 10, 10)
        assert False
    except ValueError:
        assert True

    # Test for ValueError on invalid expression
    try:
        nt.newton("xy", 10, 10)
        assert False
    except ValueError:
        assert True

    # Test for ValueError on invalid expression
    try:
        nt.newton("sin(x)sin(x)", 10, 10)
        assert False
    except ValueError:
        assert True

    print("All tests passed...")
