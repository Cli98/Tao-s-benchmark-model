*only store utility Macro function in 1st phase.;
libname repro '/folders/myshortcuts/myfolder/repro/buildModel/InitialPhase/';
%MACRO nprint(dsname);
	proc sql INOBS=100;
		select * from repro.&dsname;
	quit;
%MEND;

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