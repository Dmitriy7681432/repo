
#include <stdlib.h>	 ///< Standard library
#include <stdint.h>  ///< Std types
#include <stdbool.h> ///< _Bool to bool
#include <string.h>	 ///< Lib for memcpy, strlen, etc
#include <stdio.h>	 ///< Lib for sprintf, printf, etc
#include <string.h>	//for func memcpy 
#define TRUE 2
int main()
{
    uint8_t array[10] = {13,2,3,4,5,6,7,8,9,10};
    uint8_t mas[10]= {0,};
    memcpy(mas,array,10);
    printf("mas1 = %d\n\r",*mas);
    for(uint8_t i =0;i<10;i++)
    {
        printf("mas = %d\n\r",mas[i]);
    }

// Массив источник данных
   unsigned char src[10]="123456";
 
   // Массив приемник данных
   unsigned char dst[10]="";

   // Копируем 6 байт из массива src в массив dst
   memcpy (dst, src, 6);

   // Вывод массива dst на консоль
   printf("dst: %s\n",dst);
}
