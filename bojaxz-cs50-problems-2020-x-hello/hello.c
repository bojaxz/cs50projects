#include <cs50.h>
#include <stdio.h>
//prompts user for their name and says hello to them
int main(void)
{
    string name = get_string("What is your name?\n");
    printf("hello, %s\n", name);
}