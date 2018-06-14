libname repro '/folders/myshortcuts/myfolder/repro/dataPreprocessing/DP7/';
options mcompilenote=all mprint mlogic;
%MACRO adadot(inname,outname,lenA,lenB,Astart,Aend,Bstart,Bend);
data repro.&outname(replace=yes);*(drop=i j k);
set repro.&inname;
array dataA[&lenA] &Astart-&Aend;
array dataB[&lenB] &Bstart-&Bend;
array combined[%eval(&lenA*&lenB)];
%let k=1;
%do i=1 %to &lenA;
	%do j=1 %to &lenB;
		combined[&k]=dataA[&i]*dataB[&j];
		%let k=%eval(&k+1);
		%end;
		%end;
run;
%MEND;

%adadot(test,out,3,2,dum1,dum3,dum4,dum5)