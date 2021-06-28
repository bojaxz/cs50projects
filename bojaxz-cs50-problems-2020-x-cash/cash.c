#include <cs50.h>
#include <stdio.h>
#include <math.h>
//programme that asks for an input of a float and returns change in the least amount of coins as possible
int main(void)
{
    //get the users input(cash)
    float cash;
	do
    {
    	cash = get_float("Change owed: ");
    }
    while (cash < 0);
    //round dollars to cents
    
	int cents = round(cash * 100);
	int coins = 0;
    
    //return the correct amount of change
	while (cents >= 25)
    {
    	cents = cents - 25; 
    	coins++;
    }
    //count # of dimes
    while (cents >= 10)
    {
    	cents = cents - 10; 
    	coins++;
    }
    //count # of nickels
    while (cents >= 5)
    {
    	cents = cents - 5; 
    	coins++;
    }
    //count # of pennies
    while (cents >= 1)
    {
    	cents = cents - 1; 
    	coins++;
    }
    //returns total amount of coins
    {
    	printf("%i\n", coins);
    }
}