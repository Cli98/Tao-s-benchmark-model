*given data>>>get data in sas format
*check the field correctly;
*have missing value at end;
libname rir '/folders/myshortcuts/myfolder/repro/dataPreprocessing/DP1/';

%MACRO readinraw/parmbuff;
	%put Syspbuff contains: &syspbuff;
    %let num=1;
    %let dsname=%scan(&syspbuff,&num);
    %let forepath = /folders/myshortcuts/myfolder/repro/dataPreprocessing/DP1/;
    %let suf = .csv;
    %do %while(&dsname ne );
		FILENAME REFFILE "&forepath.&dsname.&suf.";
		PROC IMPORT DATAFILE=REFFILE
			DBMS=CSV replace
			OUT=rir.&dsname;
			GETNAMES=YES;
		RUN;
		PROC print DATA=rir.&dsname (obs=5); 
		RUN;
        %let num=%eval(&num+1);
        %let dsname=%scan(&syspbuff,&num);
        %end;	
%MEND;

%readinraw(temperature,loadf);