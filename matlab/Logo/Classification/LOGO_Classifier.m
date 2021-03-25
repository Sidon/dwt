function LOGO_Classifier(No_RandomFeature)

% MAIN FUNCTION: main function for LOGO algorithm used for classification
%========================================================
%Y. Sun, S. Todorovic, and S. Goodison, 
%Local Learning Based Feature Selection for High Dimensional Data Analysis
%IEEE Trans. on Pattern Analysis and Machine Intelligence, vol. 32, no. 9, pp. 1610-1626, 2010.
%Yijun Sun @University of Florida
%LUD: March 16, 2012
%% ========================================================
close all
disp(['>>> The number of irrelevant features is ' num2str(No_RandomFeature) '...'])

%% load data
eval(['load banana_train_data.asc'])
eval(['load banana_train_labels.asc'])
eval(['load banana_test_data.asc'])
eval(['load banana_test_labels.asc'])

eval(['train_patterns = banana_train_data;']);
train_patterns = train_patterns'; % Each column is a pattern.
eval(['train_targets = banana_train_labels;']);
eval(['test_patterns = banana_test_data;']);
test_patterns = test_patterns';
eval(['test_targets = banana_test_labels;']);

N = length(train_targets);                              % Number of patterns
Original_dim = size(train_patterns,1);                  % Number of original features
train_patterns = [train_patterns; randn(No_RandomFeature,N)]; % Add some irrelevant features
test_patterns = [test_patterns; randn(No_RandomFeature,length(test_targets))]; % treat test data in the same way
dim = size(train_patterns,1);                           % Data dimenionality

%Preprocess the data: 'unif' tranform each feature into [0, 1]
[MIN,I] = min(train_patterns,[],2);
[MAX,I] = max(train_patterns,[],2);  
for n=1:dim
    train_patterns(n,:) = (train_patterns(n,:)-MIN(n))/(MAX(n)-MIN(n));
    test_patterns(n,:) = (test_patterns(n,:)-MIN(n))/(MAX(n)-MIN(n));
end

figure(1)
plot(train_patterns(1,(train_targets==-1)),train_patterns(2,(train_targets==-1)),'o','MarkerSize',10);
hold on
plot(train_patterns(1,(train_targets==1)),train_patterns(2,(train_targets==1)),'r*','MarkerSize',10);
axis square
title('The first two useful features')
axis square;axis tight
boldify1
drawnow

%% Feature selection
%I arbitary set kernel width to 2 and regularization parameter to 1. The two parameter can be estimated through cross validation.
Para4Logo.plotfigure = 1;     % 1: plot of the result of each iteration; 0: do not plot
Para4Logo.sigma = 2 ; sigma = 2;% kernel width
Para4Logo.lambda = 1; %regularization parameter 
Para4Logo.distance = 'block';
s = cputime;
Weight = Logo(train_patterns, train_targets, Para4Logo);
CPUTime = cputime-s;
disp(['>>> The total CPU time for feature selection is ' num2str(CPUTime) ' seconds.'])

figure(3);
semilogx(Weight/max(Weight),'-o','LineWidth',1,'MarkerFaceColor','w','MarkerSize',10)
hold on
plot([Original_dim,Original_dim],[0,1],'r--', 'LineWidth',2);
xlabel('Features')
ylabel('Feature Weights')
title('Feature Weights');
axis tight
boldify1

%% classification
index_1 = find(train_targets==-1);N(1) = length(index_1);
index_2 = find(train_targets==+1);N(2) = length(index_2);
patterns_1 = train_patterns(:,index_1);
patterns_2 = train_patterns(:,index_2);
Weight = Weight(:);
Pro = [];

for n = 1:size(test_patterns,2)
    test = test_patterns(:,n);
    temp = abs(patterns_1-test*ones(1,N(1)));
    dist_1    = (Weight)'*temp;
    prob_1 = exp(-dist_1/sigma);prob_1 = prob_1/sum(prob_1);
    
    temp = abs(patterns_2-test*ones(1,N(2)));
    dist_2    = (Weight)'*temp;
    prob_2 = exp(-dist_2/sigma);prob_2 = prob_2/sum(prob_2);
    
    rho = sum(dist_1.*prob_1)-sum(dist_2.*prob_2);
    Pro(n) = 1/(1+exp(-rho));
end

%Computer testing error
Prediction = sign(Pro-0.5);
Test_Error = length(find(Prediction(:)~=test_targets(:)))/length(test_targets);
disp(['>>> The test error is ' num2str(Test_Error*100) '%.'])

%% visulization
disp(['>>> visulizing the decision boundary...'])

%prepare  data
[X,Y] = meshgrid(0:0.01:1);
for i = 1:size(X,1)
    for j = 1:size(X,1)
        test = [X(i,j);Y(i,j)];
        temp = abs(patterns_1(1:2,:)-test*ones(1,N(1)));
        dist_1    = (Weight(1:2))'*temp;
        prob_1 = exp(-dist_1/sigma);prob_1 = prob_1/sum(prob_1);
        
        temp = abs(patterns_2(1:2,:)-test*ones(1,N(2)));
        dist_2    = (Weight(1:2))'*temp;
        prob_2 = exp(-dist_2/sigma);prob_2 = prob_2/sum(prob_2);
        
        rho = sum(dist_1.*prob_1)-sum(dist_2.*prob_2);
        P(i,j) = 1/(1+exp(-rho));
    end
end

figure(4)
[C,h] =contourf(X,Y,P);%,[0.5,0.5])
hold on
plot(patterns_1(1,:),patterns_1(2,:),'o','MarkerSize',8);
plot(patterns_2(1,:),patterns_2(2,:),'r*','MarkerSize',8);
axis square
title('Decision Boundary')
set(h,'ShowText','on','TextStep',get(h,'LevelStep')*2)
colormap autumn
return
%% ==================END of THE CODE==========================















