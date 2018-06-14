libname repro '/folders/myshortcuts/myfolder/repro/buildModel/thirdPhase/';
%include '/folders/myshortcuts/myfolder/repro/buildModel/thirdPhase/auto.sas';
*check effect of trend;
%MACRO addseq(n);
*repro.mapesum should be unique in each stage;
proc sql inobs=&n;
select obs 
into :seq1 - :seq&n
from repro.mapesum;
quit;
%MEnd;

%MACRO modifyinput(id,id2);
*this function is required to pick items in seq1-id
add them up and average temperature.;
*output:cvtemperature&id1;
*delete 4 vars afterwards;
*initial dataset rename to repro.temperature;
*NOTE: 1ST DATASET SHOULD START WITH SEQ1;
%addseq(&id);*Given num now;
%traintemperature(&seq1);*initial storage;
%testtemperature(&seq1);
%trainload(&id2);*initial storage;
%testload(&id2);*will not use this in train process;
Data comb;
set traintemperature&seq1(drop=tems temc);
run;
Data testcomb;
set testtemperature&seq1(drop=tems temc);
run;
*fill in solved dataset to run;
*TO DO: Modify input process to auto-form data; 
%do n=2 %to &id;
		%traintemperature(&&&seq&n);
		%testtemperature(&&&seq&n);
		*step1: take care of trainset;
		proc sql;
		create table comb as
		select a.*,a.tem+b.tem as temp
		from comb as a
		left join traintemperature&&&seq&n as b on a.year=b.year and a.month=b.month and 
		a.day = b.day and a.hour=b.hour;
		quit;
		
		Data comb;
		set comb(drop=tem);
		run;
		
		proc datasets lib=work;
		modify comb;
		rename temp=tem;
		run;
		*step2: take care of testset;
		proc sql;
		create table testcomb as
		select a.*,a.tem+b.tem as temp
		from testcomb as a
		left join testtemperature&&&seq&n as b on a.year=b.year and a.month=b.month and 
		a.day = b.day and a.hour=b.hour;
		quit;
		
		Data testcomb;
		set testcomb(drop=tem);
		run;
		
		proc datasets lib=work;
		modify testcomb;
		rename temp=tem;
		run;
	%end;
*step3: take care of temperature reform of trainset;
proc sql;
create table rawdata as
select *,tem/&id as temp from comb;
quit;
Data rawdata;
set rawdata(drop=tem);
run;
proc datasets lib=work;
modify rawdata;
rename temp=tem;
run;
proc sql;
create table rawdata&id as
select *,tem**2 as tems,tem**3 as temc from rawdata;
quit;

*step4: take care of temperature reform of testset;
proc sql;
create table testrawdata as
select *,tem/&id as temp from testcomb;
quit;
Data testrawdata;
set testrawdata(drop=tem);
run;
proc datasets lib=work;
modify testrawdata;
rename temp=tem;
run;
proc sql;
create table testrawdata&id as
select *,tem**2 as tems,tem**3 as temc from testrawdata;
quit;
%auto(rawdata&id,tem,&id);
%auto(testrawdata&id,testtem,&id);
%trainconcat(&id,&id2);
data testtem&id;
set testtem&id(drop=station_id year month day weekday hour);
run;
proc append base=insample&id&id2 data=testtem&id;
run;
*output: insample&id&id2;
%infittest(&id,&id2);
%MEND;
	
*revise this function;
*for varName changes;
%MACRO trainconcat(id,id2);
data insample&id&id2(drop=station_id year month day weekday hour);
set tem&id;
set trainload&id2;
run;
%Mend;

%MACRO infittest(id1,id2);
	%obtainparaEx(work,insample&id1&id2,load);
	data insample&id1&id2;
	set insample&id1&id2(drop=trend);
	run;
	proc sql;
	create table insample&id1&id2 as
	select monotonic() as trend,* from insample&id1&id2;
	quit;
	proc reg data=insample&id1&id2;
	model load = &ivars;
	output out=res predicted=ypre;
	run; 
	proc sql;
		create table temp as
		select monotonic() as id,ypre from res
		where load=.;
	quit;
	proc sql;
		create table temp2 as
		select monotonic() as id,load from testload&id2;
	quit;
	proc sql;
		create table cb as
		select temp.ypre,temp2.load
		from temp,temp2
		where temp.id = temp2.id;
	quit;
	proc sql;
	create table MAPE as
	select distinct sum(abs((load-ypre))/load)/count(*)*100 as mape
	from cb;
	quit;

	%if not %sysfunc(exist(repro.testMAPEsum)) %then %do;
	proc sql;
	create table repro.testMAPEsum as
		select * from MAPE;
	%end;
	%else %do;
	proc append base=repro.testMAPEsum data=MAPE;
	run;	
	%end;
%Mend;

%MACRO loopAtest(zone,id);
	%iniseq();
	%trainload(&zone);*name: trainload&id;
	%testload(&zone);*name: cvload&id;
	%modifyinput(&id,&zone);
%Mend;

%MACRO trainload(id);
proc sql;
%if not %sysfunc(exist(trainload&id)) %then %do;
create table trainload&id as
	select year,load from repro.load
	where zone_id = &id and (year=2006 or year=2005);
%end;
%MEND;

%MACRO traintemperature(id);
proc sql;
%if not %sysfunc(exist(traintemperature&id)) %then %do;
create table traintemperature&id as
	select * from repro.temperature
	where station_id=&id and (year=2006 or year=2005);
%end;
%Mend;

%MACRO testload(id);
proc sql;
%if not %sysfunc(exist(testload&id)) %then %do;
create table testload&id as
	select year,load from repro.load
	where zone_id = &id and year=2007;
%end;
%MEND;

%MACRO testtemperature(id);
proc sql;
%if not %sysfunc(exist(testtemperature&id)) %then %do;
create table testtemperature&id as
	select * from repro.temperature
	where station_id=&id and year=2007;
%end;
%Mend;

%MACRO iniseq();
	%do n=1 %to 11;
	%global seq&n;
	%end;
%MEnd;

%MACRO obtainparaEx(dsname,tname,ex);
	%global ivars;
	proc sql;
	select name into :ivars separated by ' '
	from dictionary.columns
	where libname eq "%upcase(&dsname)"      /*library name        */
	  and memname eq "%upcase(&tname)"      /*data set name       */
	  and name    ne "&ex"    /*exlude dep variable */ ;
quit;
%MEND