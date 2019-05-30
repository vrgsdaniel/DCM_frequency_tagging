spm('defaults', 'eeg');

S = [];
S.dataset = 'C:\Users\dvargas\Documents\bccn\soekadar\lab_rotation\binocular_frequency_tagging\sham2104\sham2104_epo.fif';
S.outfile = 'spmeeg_sham_epo';
S.channels = 'all';
S.timewin = [];
S.blocksize = 3276800;
S.checkboundary = 1;
S.eventpadding = 0;
S.saveorigheader = 0;
S.conditionlabels = {'Undefined'};
S.inputformat = [];
S.mode = 'epoched';
D = spm_eeg_convert(S);


