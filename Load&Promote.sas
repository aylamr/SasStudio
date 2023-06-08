proc cas;
lib="casuser";
    table.fileInfo / caslib=lib; *to see data source files;
	table.tableInfo / caslib=lib; *to see in-memory tables;
quit;

proc cas;
	/* Create array with table names and load them in cas using a loop */
	tablestoload={"CODE_INSEE", "ACCIDENTS-CORPORELS", "TABLE_PC_PRICING_ABT_RAW"};

	do x over tablestoload;
		table.loadTable / path=x||".sashdat", caslib="casuser", 
			casout={caslib="casuser", name=x, replace=TRUE};
		table.promote / caslib="casuser", name=x, target=x, targetLib="casuser";
	end;
quit;







