libname repro '/folders/myshortcuts/myfolder/repro/buildModel/secondPhase/';
%include '/folders/myshortcuts/myfolder/repro/buildModel/secondPhase/auto.sas';
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
%addseq(&id);*return seq1-id;
%traintemperature(&seq1);*initial storage;
%cvtemperature(&seq1);
%trainload(&id2);*initial storage;
%cvload(&id2);*will not use this in train process;
Data comb;
set traintemperature&seq1(drop=tems temc);
run;
Data cvcomb;
set cvtemperature&seq1(drop=tems temc);
run;
*fill in solved dataset to run;
*TO DO: Modify input process to auto-form data; 
%do n=2 %to &id;
		%traintemperature(&&&seq&n);
		%cvtemperature(&&&seq&n);
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
		*step2: take care of cvset;
		proc sql;
		create table cvcomb as
		select a.*,a.tem+b.tem as temp
		from cvcomb as a
		left join cvtemperature&&&seq&n as b on a.year=b.year and a.month=b.month and 
		a.day = b.day and a.hour=b.hour;
		quit;
		
		Data cvcomb;
		set cvcomb(drop=tem);
		run;
		
		proc datasets lib=work;
		modify cvcomb;
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

*step4: take care of temperature reform of cvset;
proc sql;
create table cvrawdata as
select *,tem/&id as temp from cvcomb;
quit;
Data cvrawdata;
set cvrawdata(drop=tem);
run;
proc datasets lib=work;
modify cvrawdata;
rename temp=tem;
run;
proc sql;
create table cvrawdata&id as
select *,tem**2 as tems,tem**3 as temc from cvrawdata;
quit;
%auto(rawdata&id,tem,&id);
%auto(cvrawdata&id,cvtem,&id);
%trainconcat(&id,&id2);
data cvtem&id;
set cvtem&id(drop=station_id year month day weekday hour);
run;
proc append base=insample&id&id2 data=cvtem&id;
run;
*output: insample&id&id2;
%infitcv(&id,&id2);
%MEND;
	
*revise this function;
*for varName changes;
%MACRO trainconcat(id,id2);
data insample&id&id2(drop=station_id year month day weekday hour);
set tem&id;
set trainload&id2;
run;
%Mend;

%MACRO infitcv(id1,id2);
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
		select monotonic() as id,load from cvload&id2;
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
	proc append base=repro.cvMAPEsum data=MAPE;
	run;	
	
%Mend;

%MACRO loopAcv(zone);
	%iniseq();
	%trainload(&zone);*name: trainload&id;
	%cvload(&zone);*name: cvload&id;
	%do id=1 %to 11;
		%modifyinput(&id,&zone);
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

%MACRO trainload(id);
proc sql;
%if not %sysfunc(exist(trainload&id)) %then %do;
create table trainload&id as
	select year,load from repro.load
	where zone_id = &id and (year=2004 or year=2005);
%end;
%MEND;

%MACRO traintemperature(id);
proc sql;
%if not %sysfunc(exist(traintemperature&id)) %then %do;
create table traintemperature&id as
	select * from repro.temperature
	where station_id=&id and (year=2004 or year=2005);
%end;
%Mend;

%MACRO cvload(id);
proc sql;
%if not %sysfunc(exist(cvload&id)) %then %do;
create table cvload&id as
	select year,load from repro.load
	where zone_id = &id and year=2006;
%end;
%MEND;

%MACRO cvtemperature(id);
proc sql;
%if not %sysfunc(exist(cvtemperature&id)) %then %do;
create table cvtemperature&id as
	select * from repro.temperature
	where station_id=&id and year=2006;
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