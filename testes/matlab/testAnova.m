%%%%%%%%
%% Teste anova (Matlab/Libsvm - http://www.csie.ntu.edu.tw/~cjlin/libsvm/)
%% Versão 0.3 = Cross Validation
%%
%% Author:  
%%    Sidon :: 2014-05-31
%%

function testAnova  
  % Path libsvm
  addpath('/home/sidon/opt/libsvm-3.18/matlab');
  
  % Pretty print
  clc  
  format long;

  X = [5.5, 2.2, 5.5, 4, 5.5; 6.1, 2.3, 6.1, 4, 6.1; 5.9, 2.2, 5.9, 4, 5.9;
         5.3, 2.2, 5.3, 4, 5.3; 6, 2.3, 6, 4, 6; 5.5, 2.1, 5.5, 4, 5.5; 
         2.2, 2.2, 2.2, 4, 2.2; 2.3, 2.3, 2.3, 4, 2.3; 4.2, 2.1, 4.2, 4, 4.2;
         2.2, 2.2, 2.2, 4, 2.2; 2, 2.3, 2, 4, 2; 2.3, 2.3, 2.3, 4, 2.3];
  
  y = [0.;0.;0.;0.;0.;0.;1.;1.;1.;1.;1.;1.];
      
  % redução dos descritores  
  pvalues = get_pvalues(X);
  Xreduced = normc(X(:, pvalues<0.05));
    
  disp('Resultados:');
  [model] = svmtrain(y, Xreduced, '-t 0 -c 1 -v 3 ' ); 
 end

function [ pvalues ] = get_pvalues(X)
  pvalues = [];
  for col = 1 : 5
    [p, t, st] = anova1([X(1:6, col),  X(7:12, col)],'','off');
    pvalues = [pvalues p];
  end  
end  