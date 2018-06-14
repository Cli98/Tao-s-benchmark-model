*Function addseq: Extract seq from given mapesum data
*input n: the current n check stations
return macro in global pool: You can use them prior to next seq call;
libname repro '/folders/myshortcuts/myfolder/repro/buildModel/fourthPhase--testload/2nd';
%include '/folders/myshortcuts/myfolder/repro/buildModel/fourthPhase--testload/2nd/infitcvModel.sas';
*%addseq(3);
*%put &seq5;
*Go next: given n,modify input set and get combined data
Function : combCvData;

*%modifyinput(7,1);
*%auto(3);
*%infitcv(7,1);
%loopAcv(21);



