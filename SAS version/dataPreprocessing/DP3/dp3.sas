libname repro '/folders/myshortcuts/myfolder/repro/dataPreprocessing/DP3/';
*Build Tao's model
*Given stationid, year month day hour(char) load,Transform to>>
*Trend,hours(int),weekday,T,T2,T3,stationid,year month day,hour(char),
only need to build on temperature set(all data available);

*here remove hour(char);
*Done;
proc sql;
	create table repro.temhalfset as
	select monotonic() as trend,*,weekday(mdy(month,day,year)) as weekday,tem**2 as tems,tem**3 as temc,
	input(substr(hour,2,length(hour)),best12.) as hours
	from rir.tempose;
run;

data repro.temhalfset;
set repro.temhalfset(drop=hour);
run;

proc datasets lib=repro;
	modify temhalfset;
	rename hours = hour;
	run;
	
proc sql;
	create table repro.loadnew as
	select *,input(substr(hour,2,length(hour)),best12.) as hours
	from repro.loadfpose;
run;

data repro.load;
set repro.loadnew(drop=hour);
run;

proc datasets lib=repro;
	modify load;
	rename hours = hour;
	run;
