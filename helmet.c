#include<reg51.h>
sbit alcohol = P0^7;
sbit IR1 = P0^1;
sbit IR2 = P0^6;
sbit crash = P0^5;
sbit led1= P3^2;
sbit led2=P3^3;
sbit buzzer=P0^0;

char str;
int i,p,q;
void delay(int x){
	for(p=0;p<x;p++)
	for(q=0;q<7500;q++);
}
void main()
{ TMOD=0x20;
	TH1=0xFD;
	SCON=0x50;
	TR1=1;
	//led1=1;
	while(!RI);
		str=SBUF;
		RI=0;
		if(str=='4')
		{
	while(1)
	 { 
		 if(IR1==1 && IR2==1)
      {
		        if(alcohol==0)
		          { 
					       led1=0;
					       buzzer=0;
				
					 SBUF='5';
				    while(TI==0);
				    TI=0;
								delay(10);
			    
	            }
			
				      else if(alcohol==1)
				         { 
									
					          SBUF='2';
				             while(TI==0);
			              	TI=0;
									 delay(10);
			             
					          led1=1;
					          buzzer=1;
                 }	
							 }
							 
						 								 
     else if(IR1==0 || IR2==0)
       
					  { SBUF='1';
				      while(TI==0);
				       TI=0;
							delay(10);
						
				 led1=0;
				buzzer=1;
        }
			
		
	
	   if(crash==0)
		  
					{ SBUF='3';
				    while(TI==0);
				    TI=0;
						delay(10);
			    
				led2=0;
		  }
			else if(crash==1)
			{
				led2=1;
			}
		}
  }
}




				
