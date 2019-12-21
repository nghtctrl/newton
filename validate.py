"""Validate Module for Newton's Method Calculator
Created on Fall 2019
CS108 Project
@author: Jiho Kim (jk249)
"""
from re import sub


def remove_whitespace(expression):
    """This function removes all whitespace from the given expression"""
    return sub(r"\s+", "", expression)


def remove_numbers(expression):
    """This function removes all numbers from the given expression"""
    return sub(r"\d+", "", expression.replace(".", ""))


def validate(expression):
    """This function determines if the expression is valid for use in the Newton's Method Calculator"""
    test_expression = remove_numbers(remove_whitespace(expression))

    valid_powers_logarithms = [
        "root", "cbrt", "sqrt", "exp", "log", "ln", ",",
    ]

    valid_trigonometric_functions = [
        "cos", "sin", "tan", "sec", "csc", "cot", "a",
    ]

    valid_operators = [
        "**", "*", "/", "+", "-", "(", ")",
    ]

    for char in valid_powers_logarithms:
        if char in test_expression:
            test_expression = test_expression.replace(char, "")

    for char in valid_trigonometric_functions:
        if char in test_expression:
            test_expression = test_expression.replace(char, "")

    for char in valid_operators:
        if char in test_expression:
            test_expression = test_expression.replace(char, "")

    # Return True if the given expression is usable, False otherwise
    if test_expression.replace("x", "") == "":
        return True
    else:
        return False


if __name__ == "__main__":
    # These variables should all be True
    v1 = validate("3*x**2 + 5 + 4*x**3 - x**2 + 9")
    v2 = validate("root(sin(x), 4) + 7*x")
    v3 = validate("asin(atan(5*x + 4))")
    v4 = validate("(5* (6 + 4**x + (9 + x)))")

    if v1 and v2 and v3 and v4:
        print("All tests passed...")
