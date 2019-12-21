"""Commandline Interface for Testing Purposes
Created on Fall 2019
CS108 Project
@author: Jiho Kim (jk249)
"""
import newton

nt = newton.Newton()

expr = input("Please enter f(x)= ")
init = float(input("Please enter initial guess (x0): "))
num_ = int(input("Please enter number of iterations: "))

lt = nt.newton(expr, init, num_)

print("")
print("Iteration 0 |", init)

for i in range(len(lt)):
    print("Iteration " + str(i + 1) + " |", lt[i])
