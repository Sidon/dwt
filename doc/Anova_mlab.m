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

numP = num2str(pValor); % Converte o p-value para string?

numer = [ ];            % ?
features1 = [ ];        % ?

[lin cln] = size(C);    % Numero de linhas e colunas da matriz de entrada
INC = lin;              % Numero de linhas (de novo ???? )

col = 1;                % ?
n = 1;                  % ?

NovC = { };             % ? 
numer = [ ];            % ?

for col = 1 : cln - 1                       % De 1 até o número de colunas da matriz de entrada
    d1 = C(1:(INC/2),col);                  % 50% (iniciais) da matriz de entrada?  
    d2 = C(((INC/2)+1):INC,col);            % 50% (finais) da matriz de entrada?
    AnalV = [d1 d2];                        % Nova Matriz é criada
    [p, t, st] = anova1(AnalV,'','off');    % Chama uma funcao do matlab, o q signfica estes parametros, p=pvalue?
    if p < pValor                           % Compara o valor retornado peal funcao ML com o valor passado 
        NovC{1,n} = C(:,col);               % Atribui alguma coisa, o que são as chaves?
        
        [c, m, h, nms] = multcompare(st,'alpha',pValor,'display','off');  % ?
        
        features1 = [features1; [c]];       % ?
        numer = [numer; [col]];             % ?
        n = n +1;
    end
    features1 = [ ];
end

A = ones(INC,length(NovC));                 % Uma matriz de Uns?

for op = 1 :length(NovC)                    % Este for é para que? 
    A(:,op) = C(:,numer(op));
end

