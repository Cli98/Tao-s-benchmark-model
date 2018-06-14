libname repro '/folders/myshortcuts/myfolder/repro/AutomaticDP';
*abstract automatic process after data have been
transposed and initialized.;
%MACRO auto();
Data temhalfset;
set repro.temset;
run;
*step1:one hot transform;
%nominal_to_binary(sm_dataset=temhalfset, sm_var=hour, sm_prefix=hour_);
%nominal_to_binary(sm_dataset=temhalfset, sm_var=weekday, sm_prefix=weekday_);
%nominal_to_binary(sm_dataset=temhalfset, sm_var=month, sm_prefix=month_);

*Remove 3 columns for linear regression predictions;
Data onehotset(drop=hour_24 weekday_7 month_12);
set temhalfset;
run;

*step2: interaction modeling;
%adadot(onehotset,hw,23,6,hour_1,hour_23,weekday_1,weekday_6);
%adadot2(hw,final,3,23,0,0,hour_1,hour_23,hour);
%adadot2(final,finalup,3,11,0,0,month_1,month_11,month);
*step3: remove unnecessary vars;
Data repro.temperature;
set finalup;
run;
Data repro.temperatureup;
set repro.temperature(drop=month day weekday hour);
run;
%MEND;
%auto()