libname repro '/folders/myshortcuts/myfolder/repro/dataPreprocessing/DP8--load aggre/';
%MACRO cload(id);
proc sql;
%if not %sysfunc(exist(cload&id)) %then %do;
create table cload&id as
	select * from repro.load
	where zone_id = &id and (year NE 2008);
%end;
%MEND;

%MACRO combload();
*drop all columns except "load";
%cload(1);*initialize load matrix;
data combld;
set cload1;
run;
%do id=2 %to 20;
	%cload(&id);
	proc sql;
	create table combld as 
	select *,a.load+b.load as totalload 
	from combld as a
	left join cload&id as b on
	a.year=b.year and a.month=b.month and a.day = b.day and a.hour=b.hour;
	quit;
	Data combld;
	set combld(drop=load);
	run;
	proc datasets lib=work;
	modify combld;
	rename totalload=load;
	run;
%end;
*output combined file: repro.loadfin;
data repro.loadfin;
set combld(drop=zone_id);
run;
%MEND;
	
