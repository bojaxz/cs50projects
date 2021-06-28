#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            RGBTRIPLE pixel = image[i][j];

            //average RGBT values for each pixel and round values
            float average = (pixel.rgbtRed + pixel.rgbtBlue + pixel.rgbtGreen) / 3.00;

            //set pixels equal to average value found in previous line
            int avg = round(average);
            image[i][j].rgbtRed = avg;
            image[i][j].rgbtBlue = avg;
            image[i][j].rgbtGreen = avg;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            //set RGBT equal to pixel
            RGBTRIPLE pixel = image[i][j];

            //Use given equation to find sepia vaules for each RGBT value
            int sepiaRed = round(.393 * pixel.rgbtRed + .769 * pixel.rgbtGreen + .189 * pixel.rgbtBlue);
            int sepiaGreen = round(.349 * pixel.rgbtRed + .686 * pixel.rgbtGreen + .168 * pixel.rgbtBlue);
            int sepiaBlue = round(.272 * pixel.rgbtRed + .534 * pixel.rgbtGreen + .131 * pixel.rgbtBlue);

            //set pixels equal to sepia value or 255 if over 255
            image[i][j].rgbtRed = (sepiaRed > 255) ? 255 : sepiaRed;
            image[i][j].rgbtGreen = (sepiaGreen  > 255) ? 255 : sepiaGreen;
            image[i][j].rgbtBlue = (sepiaBlue  > 255) ? 255 : sepiaBlue;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    //Create temp image
    RGBTRIPLE temp[height][width];

    //Set reflection equal to temp. Will create a new image as a temp that will be copied to original image. Itterate from right to left
    for (int i = 0; i < height; i++)
    {
        int current = 0;
        for (int j = width - 1; j >= 0; j--, current++)
        {
            temp[i][current] = image[i][j];
        }
    }

    //copy temp values into image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = temp[i][j];
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    //create temp image
    RGBTRIPLE temp[height][width];

    for (int row = 0; row < height; row++)
    {
        for (int col = 0; col < width; col++)
        {
            // find the 3x3 box of pixels surronding current pixel
            int count = 0;
            int rowCoord[] = { row - 1, row, row + 1 };
            int colCoord[] = { col - 1, col, col + 1 };
            float totalred = 0, totalgreen = 0, totalblue = 0;

            //check border perimeter
            for (int r = 0; r < 3; r++)
            {
                for (int c = 0; c < 3; c++)
                {
                    int curRow = rowCoord[r];
                    int curCol = colCoord[c];

                    //gather new total for each color of pixel. Will use this as color total for average
                    if (curRow >= 0 && curRow < height && curCol >= 0 && curCol < width)
                    {
                        RGBTRIPLE pixel = image[curRow][curCol];

                        totalred += pixel.rgbtRed;
                        totalgreen += pixel.rgbtGreen;
                        totalblue += pixel.rgbtBlue;
                        count++;
                    }
                }
            }

            //Set temp image to blurred values
            temp[row][col].rgbtRed = round(totalred / count);
            temp[row][col].rgbtGreen = round(totalgreen / count);
            temp[row][col].rgbtBlue = round(totalblue / count);
        }
    }
    
    //copy temp to image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = temp [i][j];
        }
    }
    return;
}