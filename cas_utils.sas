/* CAS */
cas MySession sessopts=(caslib=casuser);
libname mycas cas caslib=casuser;


/*Determine Active Sessions*/
cas _all_ list;

/*CAS libraries*/
caslib _all_ assign;

/*LIST Files*/
proc casutil;
   list files;
run;

/*LIST Tables*/
proc casutil;
   list tables;
run;

/*Load data from caslib*/
proc casutil incaslib="casuser";
  	load casdata="ADRESSE_PARIS.sashdat"    
	casout="ADRESSE_PARIS" promote;
run; 


/*Promote data from libname*/
proc casutil;
load casdata="STOCK_PRICE.sashdat" incaslib="casuser" 
outcaslib="SWEE" casout="STOCK_PRICE" promote;
run;

/*Terminate Active Sessions*/
cas MySession terminate;







