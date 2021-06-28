// Implements a dictionary's functionality

#include <stdbool.h>
#include <string.h>
#include <strings.h>
#include <cs50.h>
#include <math.h>
#include <stdlib.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = LENGTH * 'z';

// Hash table
node *table[N];

//value for size. Total number of words of dictionary
int total_size = 0;

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // Check to see if the word is in the dictionary by checking it with words in the dictionary
    //hash the word taken
    int index = hash(word);
    
    node *cursor = table[index];
    
    while (cursor != NULL)
    {
        if ( strcasecmp(cursor->word, word) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    int sum;
    // simple has function to convert word, regardless of capitialization into a number or index
    for(int i =0; i < strlen(word); i++)
    {
        sum = tolower(word[i]);
        sum++;
    }
    return (sum % N);
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Load function to load dictionary
    //open dictionary file
    FILE *file = fopen(dictionary, "r" );
    if (!file)
    {
        return false;
    }

    //begin setup to copy words from dictionary
    char word[LENGTH + 1];
    while (fscanf(file, "%s", word) != EOF)
    {
        //create space for each word by allocating space via a new node
        node *new_node = malloc(sizeof(node));
        if (new_node == NULL)
        {
            return false;
        }

        //copy word into new node
        strcpy(new_node->word, word);
        new_node->next = NULL;

        //hash word using hash function to assign index to word
        int index = hash(word);

        if(table[index] == NULL)
        {
            table[index] = new_node;
        }
        else
        {
            new_node->next = table[index];
            table[index] = new_node;
        }
        //increment size every time a new number is added
        total_size++;
    }
    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    // return the value of size that was found in load
    return total_size;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    // TODO
    //we need to free any memory to free memory allocated by using malloc
    //we need to unload each linked list and each node
    //need a secondary variable
    for (int i =0; i < N; i++)
    {
        node *head = table[i];
        node *cursor = head;
        node *tmp = head;
        
        while(cursor != NULL)
        {
            cursor = cursor->next;
            free(tmp);
            tmp = cursor;
        }
    }
    //then check to make sure that memory was freed
    return true;
}