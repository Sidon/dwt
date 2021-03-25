function [ numer, A, numAtribut, numAtributReduzido] = attribAnova(C,pValor,dirAtribut)
%{
%% function [ARQUIVOWEKA] = CriaConjuntos(CAMIN,INC, IMAGENS,ARQUIVO);
%%
%% Author:
%%   PhD. Marcelo Zanchetta do Nascimento (marcelo.nascimento@ufabc.edu.br)
%%
%% Author:
%%   Ms. Rogério Daniel Dantas
%%
%% Date:    November - 2010 Course:  Information Engineering (Federal
%% University of ABC)
%%
%% ______________________________ Function ________________________________
%%
%% Separa as imagens CC's das MLO's gerando arquivo .ARFF para WEKA
%%
%% ___________________________ Input Parameters ___________________________
%%
%%
%%  C - Matriz ( Image )
%%  pValor - Indice de significância da ANOVA
%%
%% ___________________________ Output Parameters __________________________
%%
%% ________________________________ Sample ________________________________
%%
%% ________________________________________________________________________
%}

numP = num2str(pValor);

numer = [ ];
features1 = [ ];

[lin cln] = size(C);
INC = lin;
%Verifica se a variação de distância é relevante
col = 1;
n = 1;
NovC = { };
numer = [ ];

for col = 1 :cln - 1
    d1 = C(1:(INC/2),col);
    d2 = C(((INC/2)+1):INC,col);
    AnalV = [d1 d2];
    [p, t, st] = anova1(AnalV,'','off');
    if p < pValor
        NovC{1,n} = C(:,col);
        [c, m, h, nms] = multcompare(st,'alpha',pValor,'display','off');
        features1 = [features1; [c]];
        numer = [numer; [col]];
        n = n +1;
    end
    features1 = [ ];
end

A = ones(INC,length(NovC));
for op = 1 :length(NovC)
    A(:,op) = C(:,numer(op));
end

[temp, numAtribut] = size(C);

[temp, numAtributReduzido] = size(A);

%disp(strcat('Reduzido: ',num2str(numAtributReduzido), ...
%    '  Total: ',num2str(numAtribut)));