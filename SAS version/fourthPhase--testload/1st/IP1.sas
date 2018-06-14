libname repro '/folders/myshortcuts/myfolder/repro/buildModel/fourthPhase--testload/1st/';
%include '/folders/myshortcuts/myfolder/repro/buildModel/fourthPhase--testload/1st/suputil.sas';
%include '/folders/myshortcuts/myfolder/repro/buildModel/fourthPhase--testload/1st/infitModel.sas';
*obtain Zone21 after execute DP8 process;
*should rename input from 'loadfin' to 'load';

%loopA(21);
%sortMAPE();



