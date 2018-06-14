libname repro '/folders/myshortcuts/myfolder/repro/dataPreprocessing/DP8--load aggre/';
%include '/folders/myshortcuts/myfolder/repro/dataPreprocessing/DP8--load aggre/support.sas';
*Task: given input transposed data, output load aggre result.
*return 4 years'(2004-2007) result;
%combload();