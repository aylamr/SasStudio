/* CAS */
cas MySession sessopts=(caslib=casuser);
libname mycas cas caslib=casuser;
proc casutil;
load data=sashelp.cars replace;
run;
data mycas.bigcars;
set mycas.cars;
do i=1 to 1000000;
output;
end;
run;
data mycas.bigcars_score;
set mycas.bigcars;
length myscore 8;
myscore=0.3*Invoice/(MSRP-Invoice)
+ 0.5*(EngineSize+Horsepower)/Weight + 0.2*(MPG_City+MPG_Highway);
Thread=_threadid_;
run;