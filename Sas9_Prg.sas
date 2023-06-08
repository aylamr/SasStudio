/*DATA step*/
/*large version of the sashelp.cars data set that has 42.8
million rows*/
data bigcars;
set sashelp.cars;
do i=1 to 1000000;
output;
end;
run;


/*new variable named myscore that is a formula
based on values within the data*/

data bigcars_score;
set bigcars;
length myscore 8;
myscore=0.3*Invoice/(MSRP-Invoice)
+ 0.5*(EngineSize+Horsepower)/Weight + 0.2*(MPG_City+MPG_Highway);
run;

