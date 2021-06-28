#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>
#define BLOCK 512

int main(int argc, char *argv[])
{
    //Print intented use of program if CLI is not 2
    if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }
    
    //open file entered in CLI
    FILE *file = fopen(argv[1], "r");

    //error message if file cannot open
    if (file == NULL)
    {
        printf("Unable to open image\n");
        return 1;
    }

    //list of variables
    typedef uint8_t BYTE;
    BYTE buffer[BLOCK];
    size_t bytes_read;
    bool is_first_jpeg = false;
    FILE *current_file;
    char current_filename[100];
    int current_filenumber = 0;
    bool found_jpeg = false;

    //while loop to determine what to do with the contents of the file
    while (true)
    {
        //buffer of memory when reading from the file or memory card
        bytes_read = fread(buffer, sizeof(BYTE), BLOCK, file);

        //break if 0 is being read. Used to cut off slack space or end of file
        if (bytes_read == 0)
        {
            break;
        }


        //if loop to find JPEG header
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer [3] & 0xf0) == 0xe0)
        {
            //if condition for first JPEG to determine behavoir for writing to a file. First JPEG will require a new file
            found_jpeg = true;
            if (!is_first_jpeg)
            {
                is_first_jpeg = true;
            }
            //when a new header is found that is not the first JPEG, we close the current file and start a new file
            else
            {
                fclose(current_file);

            }
            //instructions to create a new file name based on current_filenumber, open the file and write to it, increment current_filenumber
            sprintf(current_filename, "%03i.jpg", current_filenumber);
            current_file = fopen(current_filename, "w");
            fwrite(buffer, sizeof(BYTE), bytes_read, current_file);
            current_filenumber++;
        }
        //continue to write to file if not first JPEG and when a header is not found 
        else
        {
            if (found_jpeg)
            {
                fwrite(buffer, sizeof(BYTE), bytes_read, current_file);
            }
        }
    }
    //close file, close current file, and end program
    fclose(file);
    fclose(current_file);
    return 0;
}