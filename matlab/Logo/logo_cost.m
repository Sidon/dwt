function cost=IMRelief_cost(alpha, P)

%Function ComputeAlpha: compute alpha using linear search
Z = P.Z;
Weight = P.Weight;
Targets = P.Targets;
descent = P.descent;
lambda = P.lambda;

Weight = Weight-alpha*descent;
a = ((Weight(:).^2)')*Z; %margin
Result = 1./(1+exp(-a)); %probability of being class 1

index = find(Result==1);
Result(index) = 1-10^(-10);
index = find(Result==0);
Result(index) = 10^(-10);

if length(find(Result==1))>=1 | length(find(Result==0))>=1
    cost = +inf;
else
    cost = -sum(Targets.*log(Result(:))+(1-Targets).*log(1-Result(:)))+lambda*((Weight(:))'*Weight(:));
end


return
