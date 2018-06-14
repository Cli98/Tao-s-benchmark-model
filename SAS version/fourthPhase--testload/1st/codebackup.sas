%macro split (name=);
data one;
%let I=1;
%do %until(%scan(&name,&I) eq );
word&i = "%scan(&name,&I)"; 
%let I=%eval(&I+1);
%end;
run;
%mend split;
%split (name=1 2 3 4 5);

proc transpose data=one
out = newone name=index;
by word1;
run;