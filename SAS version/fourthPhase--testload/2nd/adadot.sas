*libname repro '/folders/myshortcuts/myfolder/repro/buildModel/secondPhase/';

%MACRO adadot(inname,outname,lenA,lenB,Astart,Aend,Bstart,Bend);
data &outname(replace=yes);*(drop=i j k);
set &inname;
array dataA[&lenA] &Astart-&Aend;
array dataB[&lenB] &Bstart-&Bend;
array hourweekday[%eval(&lenA*&lenB)];
%let k=1;
%do i=1 %to &lenA;
	%do j=1 %to &lenB;
		hourweekday[&k]=dataA[&i]*dataB[&j];
		%let k=%eval(&k+1);
		%end;
		%end;
run;
%MEND;
%MACRO adadot2(inname,outname,lenA,lenB,Astart,Aend,Bstart,Bend,type);
data &outname(replace=yes);*(drop=i j k);
set &inname;
array dataA[&lenA] tem tems temc;
array dataB[&lenB] &Bstart-&Bend;
array tem&type[%eval(&lenA*&lenB)];
%let k=1;
%do i=1 %to &lenA;
	%do j=1 %to &lenB;
		tem&type[&k]=dataA[&i]*dataB[&j];
		%let k=%eval(&k+1);
		%end;
		%end;
run;
%MEND;