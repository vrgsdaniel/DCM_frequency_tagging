spm('defaults','EEG');
%--------------------------------------------------------------------------
% Data filename
%--------------------------------------------------------------------------
DCM.xY.Dfile  = 'C:\Users\dvargas\Documents\bccn\soekadar\lab_rotation\binocular_frequency_tagging\DCM_frequency_tagging\sham2104\spmeeg_sham_dominances_epo.mat';
DCM.xY.modality  = 'EEG'; 
DCM.name = 'C:\Users\dvargas\Documents\bccn\soekadar\lab_rotation\binocular_frequency_tagging\DCM_frequency_tagging\DCMs\4Modes\full_model\DCM3005_3inputs.mat';

%--------------------------------------------------------------------------
% Parameters and options used for setting up model
%--------------------------------------------------------------------------
DCM.options.analysis = 'IND';
DCM.options.model = 'ERP';
DCM.options.spatial =  'ECD';
DCM.options.trials = [1 2];
DCM.options.Tdcm = [-50 400] ;
DCM.options.Fdcm = [9 17];
DCM.options.Rft = 20;
DCM.options.onset = 64;
DCM.options.dur = 16;
DCM.options.Nmodes = 4 ;
DCM.options.h = 1;
DCM.options.han = 0 ;
DCM.options.D = 1;
DCM.options.lock = 0 ;
DCM.options.multiC = 0 ;
DCM.options.location = 0 ;
DCM.options.symmetry = 0;

%--------------------------------------------------------------------------
% Between trial effects
%--------------------------------------------------------------------------

DCM.xU.X = [0; 1];
DCM.xU.name = {'switch'};

%--------------------------------------------------------------------------
% Data and spatial model
%--------------------------------------------------------------------------

DCM = spm_dcm_erp_data(DCM);

%--------------------------------------------------------------------------
% Location priors for dipoles
%--------------------------------------------------------------------------
DCM.Lpos  = [[0; -92; 10] [-33; -67; 30] [33; -67; 30] [-50; -6; -36] [50; -6; -36] [-18; 62; 0] [18; 62; 0]];
DCM.Sname = {'v1', 'left v5', 'right v5', 'left it', 'right it', 'left pfc', 'right pfc'};
Nareas    = size(DCM.Lpos,2);

%--------------------------------------------------------------------------
% Spatial model
%--------------------------------------------------------------------------

DCM = spm_dcm_erp_dipfit(DCM);

%--------------------------------------------------------------------------
% Specify connectivity model
%--------------------------------------------------------------------------

DCM.A{1} = zeros(Nareas,Nareas);
DCM.A{1}(1, 2) = 1;
DCM.A{1}(1, 3) = 1;
DCM.A{1}(2, 1) = 1;
DCM.A{1}(2, 4) = 1;
DCM.A{1}(3, 1) = 1;
DCM.A{1}(3, 5) = 1;
DCM.A{1}(4, 2) = 1;
DCM.A{1}(4, 6) = 1;
DCM.A{1}(4, 7) = 1;
DCM.A{1}(5, 3) = 1;
DCM.A{1}(5, 6) = 1;
DCM.A{1}(5, 7) = 1;
DCM.A{1}(6, 4) = 1;
DCM.A{1}(6, 5) = 1;
DCM.A{1}(7, 4) = 1;
DCM.A{1}(7, 5) = 1;

DCM.A{2} = DCM.A{1} + eye(7);
DCM.A{3} = zeros(Nareas,Nareas);

DCM.B{1} = zeros(Nareas,Nareas);
DCM.C = [1; 0; 0; 0; 0; 0 ; 0];

%--------------------------------------------------------------------------
% Invert
%--------------------------------------------------------------------------

DCM      = spm_dcm_ind(DCM);