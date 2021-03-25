function Weight = Logo(patterns, targets, Para)

%Logo: logo algorithm
%Y. Sun, S. Todorovic, and S. Goodison, 
%Local Learning Based Feature Selection for High Dimensional Data Analysis
%IEEE Trans. on Pattern Analysis and Machine Intelligence, vol. 32, no. 9, pp. 1610-1626, 2010.
%--------------------------------------------------------------------------
%INPUT:
%     patterns:  training data: [x1,x2,...xn] Each column is an observation
%      targets:  class label = {1,2}
%         Para:  parameters. 
%Para.distance:  distance metric (default: block distance)
%   Para.sigma:  kernel width
%  Para.lambda:  regulariztion parameter
%    Para.plot:  1: plot of the learning process; 0: do not plot
%OUTPUT:
%       Weight:  weight of features
%--------------------------------------------------------------------------
%by Yijun Sun @University of Florida
%update history: Feb. 10/March 20, 2007/OCT 10, 2010
%% ==========================================================================

distance = Para.distance; % distance metric
sigma = Para.sigma;       % kernel width
lambda = Para.lambda;     % regulariztion parameter
plotfigure = Para.plotfigure;         %whether the progress and feature weights are plotted
%--------------------------------------------------------------------------

Uc = unique(targets);
if min(Uc)==-1
    targets = targets/2+1.5; % transform targets into {1,2}
end
Targets = targets-1;
[dim,N_patterns] = size(patterns);      % Data dimenionality

for n=1:length(Uc)
    temp = find(targets==n);
    index{n} =temp;
    N(n) = length(temp);
end

Original_dim = dim;
Original_index = 1:dim;
index_0 = find(Targets==0);
History = [];
Weight =  ones(dim,1);
History(:,1) = Weight;
P.lambda = lambda;
P.Targets = Targets(:);
% -------------------------------------------------------------------------

Difference =1;
t=0;
theta =[];
while  Difference>0.01 & t<=10;
    t=t+1;
    NM = zeros(dim,N_patterns);
    NH = zeros(dim,N_patterns);
 
    for i = 1:N_patterns,
        Prob_dif = 0;
        Prob_same = 0;

        for c = 1:length(Uc)
            switch lower(distance)
                case {'euclidean'}
                    Temp            = (patterns(:,index{c}) - patterns(:,i)*ones(1,N(c))).^2;
                case {'block'}
                    Temp            = abs(patterns(:,index{c}) - patterns(:,i)*ones(1,N(c)));
            end

            if t==1
                dist    = sum(Temp,1)/sqrt(dim);
            else
                dist    = (Weight(:).^2)'*Temp;
            end
            temp_index = find(dist==0);
            
            %calculate probabilities
            prob = exp(-dist/sigma);
            if ~isempty(temp_index);prob(temp_index(1)) = 0;end
            if sum(prob)~=0;prob_1 = prob/sum(prob);else;[dum,I] = sort(dist);prob(I(2))=1;prob_1=prob;end
                        
            if targets(i)==c;
                NH(:,i) = Temp*prob_1(:);
            end
            if targets(i)~=c;
                NM(:,i) = NM(:,i)+ Temp*prob_1(:);%*Prioi(c)/(1-Prioi(targets(i)));
            end
        end
    end
    
    Z = NM-NH;
    Z(:,index_0) = -Z(:,index_0);
    CostDiff = 1000; Cost(1) =10000;
    j=1;

    while CostDiff>0.01*Cost(j) 
        j= j+1;
        a = ((Weight(:).^2)')*Z; % Margin
        Result = 1./(1+exp(-a)); % Probability of being class 1
        difference = Result(:)-Targets(:);
        descent = (Z*difference(:)).*Weight+lambda*Weight;

        %line search to find alpha    
        P.Z = Z;
        P.Weight = Weight;
        P.descent = descent;
        [alpha,Cost(j)] = fminbnd('logo_cost', 0, 1, optimset('TolX',0.02), P); 

        Weight = Weight-alpha*descent;
        CostDiff = abs(Cost(j)-Cost(j-1));
    end
    
    Weight = abs(Weight);
    Difference = norm(abs(Weight/max(Weight)-History(:,t)/max(History(:,t))));%max(abs(Weight/max(Weight)-History(:,t)/max(History(:,t))));
    theta(t) = Difference;
    History(:,t+1) = Weight;  
    
    if t==1;index_zeros = find(Weight<=10^(-5));end
    if t>=2;index_zeros = find(Weight<=10^(-5));end
    patterns(index_zeros,:)=[];
    dim = size(patterns,1);
    Weight(index_zeros)=[];
    History(index_zeros,:)=[];
    Original_index(index_zeros)=[];
end
temp = zeros(1,Original_dim);
temp(Original_index) = Weight.^2;
Weight = temp;

%Monitoring the feature weights
if plotfigure ==1
    figure;
    semilogy(theta,'-o','LineWidth',1,'MarkerFaceColor','w','MarkerSize',10)
    title('Theta');
    xlabel('Number of Iterations');
    ylabel('Difference')
    grid on
    boldify1
    drawnow
end

return
%% ==================End of the code===================================





