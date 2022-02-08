#ifndef MAIN_H
#define MAIN_H
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <stdint.h>
#include <unistd.h>


typedef struct st_pop{

	int id;
	int (*func1)(int arg);

}pop;


typedef struct st_pop2{


	int (*func2)(struct st_pop* arg, int lol);

}pop2;

typedef struct st_pop1{

	pop *pow;
	pop2 *pow2;
	int (*func)(struct st_pop1* arg, float rol);
	void (*pass)(struct st_pop1* arg, int top);

}pop1;








#endif // MAIN_H
