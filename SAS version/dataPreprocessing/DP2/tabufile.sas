libname rir '/folders/myshortcuts/myfolder/repro/dataPreprocessing/DP2/';
proc transpose data=rir.loadf
      out=rir.loadfpose
      name=hour
      prefix=load;
      by zone_id year month day;
run;

proc transpose data=rir.tem
      out=rir.tempose
      name=hour
      prefix=tem;
      by station_id year month day;
run;

proc datasets lib=rir;
	modify loadfpose;
	attrib _all_ label=' ';
	rename load1 = load;
	run;
	
proc datasets lib=rir;
	modify tempose;
	attrib _all_ label=' ';
	rename tem1 = tem;
	run;