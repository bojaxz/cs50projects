from cs50 import get_string

# define get number function to get card number from the user
number = get_string("Please enter your card number:")

# compare first character of string with different card types
if number[0:1] == "3" and "7":
    print("AMEX")

elif number[0] == "5":
    print("MASTERCARD")

elif number[0] == "4":
    print("VISA")

else:
    print("INVALID")

