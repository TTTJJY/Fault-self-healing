%========================================================================
% Author:  Nina Thornhill
%          Department of Electronic and Electrical Engineering
%          University College London
%          Torrington Place
%          London WC1E 7JE
%========================================================================
% InitializeCSTHDisturbedStdOp2: initializes the Simulink simulation called CSTHDisturbedStdOp2.mdl
% It places values of the numerical parameters and initial state into the Matlab
% workspace. 
% Reference: 
% Thornhill, N.F., Patwardhan, S.C and Shah, S.L., 2007, Stirred tank heater simulation 
% with experimental data, submitted to Journal of Process Control, special issue 
% honouring Dale Seborg. 
%========================================================================

%========================================================================
% Initial values for the time delay block outputs in the pilot plant model 
TempDegCIC = 42.516529; CWValveIC = 7.704263;

%========================================================================
% Values of initial state. The Initial state tab in the Simulation Parameters pull-down menu 
% in the Simulink model CSTHDisturbedStdOp2.mdl must be ticked to make use of these. 
xInitial = [3.308550185873605e-003
    7.329951310877581e+000
    2.927619996753882e+001
    7.704263149352320e+000
    6.053218730743541e+000
    5.832988992651696e+002];


% The states are
%     '.../Pilot Plant Model/Mass balance with level disturbance/Integrator'
%     '.../level PID/Integrator'
%     '.../Pilot Plant Model//CW valve with CW disturbance/Valve dynamics/Transfer Fcn'
%     '.../flow PID/Integrator'
%     '.../temp PID/Integrator'
%     '.../Pilot Plant Model/Heat balance/OUT_H'

% If the Simulink model is edited then the values of the states, their ordering and 
% even the number of states may change. The new steady state can be determined by 
% un-ticking the Initial state tab in the Simulation Parameters pull-down menu and 
% running the new simulation to a steady state. The steady state xFinal in the 
% workspace should be cut-and-pasted into this m-file for use as xInitial in the next run.  

%========================================================================
% A useful debugging line to find the state descriptions in xstord
% [sizes, x0, xstord] = CSTHDisturbedStdOp2([],[],[],0)
% The strings defining the states are accessed as follows:
% xstord{1}    %... and so on
%========================================================================

% Update, May 30th 2013:
% A warning message might appear: 
% Warning: Initializing the model 'CSTHDisturbedStdOp2' with the initial state
% specified in array format is not recommended.
% The array format does not contain information about how the specified states are
% associated with the respective blocks. Since the sorted order may change under
% different conditions, such associations are necessary for achieving consistent
% results. Therefore, consider initializing the states using a structure format.

% If you want to suppress  warning messages related to the above comments
% then load the model first, then type the following command at the Matlab
% prompt:
% set_param('CSTHDisturbedStdOp2', 'InitInArrayFormatMsg', 'None')



