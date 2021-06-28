#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <string.h>
#include <math.h>

int l;
int w;
int s;


int main(void)
{
    //get input text from user
    string text = get_string("What is the text?: \n");

    //set length of text
    int len = strlen(text);

    //add one if text starts with alnum
    if (isalnum(text[0]))
    {
        w = 1;
    }
    //count number of letters

    for (int i = 0; i < len; i++)
    {
        //count letters
        if (isalpha(text[i]))
        {
            l++;
        }
        //count words
        if (i < len - 1 && isspace(text[i]) && (isalnum(text[i + 1]) || text[i + 1] == '"'))
        {
            w++;
        }
        //count sentances
        if (i > 0 && (text[i] == '!' || text[i] == '?' || text[i] == '.') && isalnum(text[i - 1]))
        {
            s++;
        }
    }
    //calculate Coleman-Liau Index
    double grade = (0.0588 * l * 100 / w - 0.296 * s * 100 / w) - 15.8;
    // int grade = round(graded);
    
    // debugger
    //printf("Letters: %i\n Words: %i\n Sentences: %i\n", l, w, s);

    //return grade
    if (grade <= 1)
    {
        printf("Before Grade 1\n");
    }
    else if (grade < 16)
    {
        printf("Grade %.0f\n", round(grade));
        //printf("Grade %f\n", grade);
    }
    else
    {
        printf("Grade 16+\n");
    }
}