#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <string.h>

bool check_key(string plain_text);

//get key from argv[]
int main(int argc, string argv[])
{
    //validate key
    //no key entered
    if (argc != 2)
    {
        printf("Usage: ./substitution KEY");
        return 1;
    }
    //check key length
    if (!check_key(argv[1]))
    {
        printf("Key must contain 26 characters.");
        return 1;
    }
    
    //get plaintext
    string plain_text = get_string("plaintext: ");
    string hash = argv[1];
    for (int i = 'A'; i <= 'Z'; i++)
    {
        hash[i - 'A'] = toupper(hash[i - 'A']) - i;
    }
    printf("ciphertext: ");
    //prints cipher text character by character by subtracting hash value.
    for (int i = 0, len = strlen(plain_text); i < len; i++)
    {
        if (isalpha(plain_text[i]))
        {
            plain_text[i] = plain_text[i] + hash[plain_text[i] - (isupper(plain_text[i]) ? 'A' : 'a')];
        }    
        printf("%c", plain_text[i]);
    }
    printf("\n");
}
//bool function to return errors
bool check_key(string plain_text)
{
    //error for key that is not 26 characters
    int len = strlen(plain_text);
    if (len != 26)
    {
        return false;
    }
    int recur[26] = {0};
    for (int i = 0; i < len; i++)
    {
        //error for non-alphabetic characters
        if (!isalpha(plain_text[i]))
        {
            return false;
        }
        int count = toupper(plain_text[i]) - 'A';
        //error for repeating characters
        if (recur[count] > 0)
        {
            return false;
        }
        recur[count]++;
    }
    
    return true;
}