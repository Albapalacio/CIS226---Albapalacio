9#Display a Welcome Message:
# Print a message to introduce the calculator program.

print("Welcome to the Simple Python Calculator!")

#Prompt the User for Input:
# Ask the user to input two numbers.
# Use float(input()) to ensure the program accepts both integers and decimals.

num1 = float(input("Enter the first number: ")) 
num2 = float(input("Enter the second number: "))

#Display Operation Options:
# Show a menu of arithmetic operations and prompt the user to choose one.

print("Choose an operation: +, -, *, /") 
operation = input("Enter your choice: ")

#Perform the Operation:
# Use if/elif/else statements to execute the operation based on the user’s choice.
# Handle division carefully (e.g., check if the divisor is zero).

if operation == "+": result = num1 + num2 
elif operation == "-": result = num1 - num2 
elif operation == "*": result = num1 * num2 
elif operation == "/": 
    if num2 != 0: result = num1 / num2 
    else: result = "Undefined (division by zero is not allowed)" 
else: result = "Invalid operation"

#Display the Result:
# Print the result to the user.

print(f"The result is: {result}")
