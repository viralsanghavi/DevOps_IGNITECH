#include<stdio.h>
void main()
{
	int a,b,var;
	printf("Enter the two numbers: \n");
	scanf("%d,%d",&a,&b);
	printf("\n Enter your choices\
		\n 1.Addition");
	printf("\n Enter the choice now:");
	scanf("%d",&var);
	switch(var)
	{
		case 1:
			printf("\n Addition is: %d \n",a+b);
			break;
		default:
			printf("\n This is the default case");
			break;

	}
}
