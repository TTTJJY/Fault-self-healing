function [CA,T]=CSTR_DIS(CA_INI,T_INI,DeltaT,qc)

% Parameters:
% Process Flowrate (m^3/sec)
q = 100;
% Feed Concentration (mol/m^3)
CA0 = 1;
% Feed Temperature (K)
T0 = 350;
% Inlet Coolant Temperature (K)
Tc0 = 350;
% Volume of CSTR (m^3)
V = 100;
% Heat Transfer Term (cal/(min K))
hA = 7e5;
% Reaction Rate Constant (min^{-1})
k0 = 7.2e10;
% E - Activation energy in the Arrhenius Equation (J/mol)
% R - Universal Gas Constant = 8.31451 J/mol-K
EoverR = 1e4;
% Heat of Reaction (cal/mol)
DeltaH = 2e5;
% Liquid Density (g/L)
rou = 1e3;
rouc = 1e3;
% Specific Heats (cal/(g K))
Cp = 1;
Cpc = 1;
% INITIALIZATION OF THE PARAMETERS
TimeLen=length(qc);
CA=zeros(TimeLen+1,1);
T=zeros(TimeLen+1,1);
CA(1)=CA_INI;
T(1)=T_INI;

for i=1:TimeLen
    CA(i+1)=CA(i)+DeltaT*(q/V*(CA0-CA(i))-k0*exp(-EoverR/T(i))*CA(i));
    T(i+1)=T(i)+DeltaT*(q/V*(T0-T(i))+DeltaH/(rou*Cp)*k0*exp(-EoverR/T(i))*CA(i)+rouc*Cpc*qc(i)/V/rou/Cp*(1-exp(-hA/(rou*Cpc*qc(i))))*(Tc0-T(i)));
end
CA=CA(2:TimeLen+1);
T=T(2:TimeLen+1);
end
