#include <cs50.h>
#include <stdio.h>
//mario based programme that will create the steps at the end of a mario level based on the users input.
int main(void)
{
    //prompt user for height
    int height;
    do
    {
        height = get_int("Height: \n");
    }
    while (height < 1 || height > 8);
    
    //build stairs according to height
    for (int x = 0; x < height; x++)
    {
        for (int z = 0; z < height - x - 1; z++)
        {    
            printf(" ");
        }
        for (int y = 0; y <= x; y++)
        {
            printf("#");
        }
        printf("\n");
    }
}