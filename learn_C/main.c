#include "main.h"
#include <conio.h>
#define SIZE 10u

//int func1(struct st_pop *arg);

int func2(struct st_pop *arg, int lol);
int func(struct st_pop1 *arg, float rol);
void pass(struct st_pop1 *arg, int top);


pop pow1;
pop2 ea1 = {func2};
pop1 ea = {&pow1,&ea1,func};

//pop pow2={0,func1};



int func2(pop *arg,int lol)
{
	lol = lol+2;

	printf("func2 %d\n", lol);

	return 0;

}

int func(pop1 *arg, float rol)
{
	printf("func\n");

	int rev=0;

	rev = rol*3000;

	return func2(arg, rev);
}

void pass(struct st_pop1 *arg, int top)
{
	func2(arg,top);
	//	printf("pass\n");
//	return 0;

}

int lol(float *lop)
{
	printf("LOP %f\n", *lop);
	int pol = (int)lop;
	printf("LOP %d\n", pol);
	return 0;
}

//int lol1(int arg)
//{
//	arg =15;
//	return lol(arg);
//}


int main()
{
	float a=50.3;



//	func(&pow1);
//	func2(&ea1);

	lol(&a);
	func(&a,a);
	pass(&a,a);

	return 0;
}
