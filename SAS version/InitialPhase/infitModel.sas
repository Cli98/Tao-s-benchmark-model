libname repro '/folders/myshortcuts/myfolder/repro/buildModel/InitialPhase/';
*perform in-sample fit in 1st stage
intermidiate values stored in matrix;

%MACRO trainload(id);
proc sql;
create table trainload&id as
	select year,load from repro.load
	where zone_id = &id and (year=2004 or year=2005);
%MEND;

%MACRO traintemperature(id);
proc sql;
create table traintemperature&id as
	select * from repro.temperature
	where station_id=&id and (year=2004 or year=2005);
%Mend;

%MACRO trainconcat(id1,id2);
data insample&id1&id2(drop=station_id year);
set traintemperature&id1;
set trainload&id2;
run;
%Mend;

%MACRO infit(id1,id2);
	%obtainparaEx(work,insample&id1&id2,load);
	proc reg data=insample&id1&id2;
	model load = &ivars;
	output out=res predicted=ypre;
	run; 
	proc sql;
		create table MAPE as
		select distinct sum(abs((load-ypre))/load)/count(*)*100 as mape
		from res;
	quit;
	proc append base=repro.MAPEsum data=MAPE;
	run;
%Mend;

%MACRO loopA(zone);
	%trainload(&zone);
	%do id=1 %to 11;
		%traintemperature(&id);
		%trainconcat(&id,&zone);
		%infit(&id,&zone);
	%end;
%Mend;

%MACRO sortMAPE();	
	proc sql;
	create table MAPEnew as
	select monotonic() as obs, * from repro.mapesum;
	quit;
	proc sort data=MAPEnew out=repro.mapesum;
	by mape;
	run;
%Mend;
*need revise;
*Do not use this function;
%MACRO mape(dsa,dsb);
proc sql;
create table mape as
	select (dsa.load-dsb.load)/dsa.load
	from dsa,dsb;
%MEND;