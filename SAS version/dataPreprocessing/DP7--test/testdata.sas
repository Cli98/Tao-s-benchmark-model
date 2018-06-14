libname repro '/folders/myshortcuts/myfolder/repro/dataPreprocessing/DP7/';
*Following blocks for test propose;
data repro.test;
    infile datalines dsd;
    input dum1 dum2 dum3 dum4 dum5;
datalines;
1,2,3,4,7
2,3,3,5,10
3,-1,5,8,7
4,5,7,8,9
;
*test past;
%adadot(test,out,3,2,dum1,dum3,dum4,dum5)