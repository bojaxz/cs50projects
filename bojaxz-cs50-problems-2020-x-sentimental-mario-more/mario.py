# import the get_int function from cs50 library
from cs50 import get_int

# define get height funtion that will get a height from the user betweem 1 and 8 inclusive.
# then reprompt the user if number is out of bounds


def get_height():
    while True:
        try:
            n = get_int("Please enter height:\n")
            if 0 < n < 9:
                return n
            else:
                print("Number not in range.")
        except ValueError:
            print("Invalid Input")

# function to build the pyramid using the int from the user in get_height


def height():
    pheight = get_height()
    h = 0
    while h < pheight:
        h += 1
        print((" " * (pheight - h)), end="")
        print(("#" * (h)), end="  ")
        print("#" * (h))


height()
